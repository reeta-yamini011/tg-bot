from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class UserRow:
    user_id: int
    first_seen: int
    last_seen: int
    username: str | None
    full_name: str | None


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA foreign_keys=ON;")
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id    INTEGER PRIMARY KEY,
                first_seen INTEGER NOT NULL,
                last_seen  INTEGER NOT NULL,
                username   TEXT,
                full_name  TEXT
            );
            """
        )
        self._conn.commit()

    def upsert_user(self, user_id: int, username: str | None, full_name: str | None) -> None:
        now = int(time.time())
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO users (user_id, first_seen, last_seen, username, full_name)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                last_seen=excluded.last_seen,
                username=excluded.username,
                full_name=excluded.full_name
            """,
            (user_id, now, now, username, full_name),
        )
        self._conn.commit()

    def total_users(self) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        (count,) = cur.fetchone()
        return int(count)

    def close(self) -> None:
        self._conn.close()
