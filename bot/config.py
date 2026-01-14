from __future__ import annotations

from dataclasses import dataclass
import os


def _split_ints(value: str) -> list[int]:
    items = []
    for part in (value or "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            items.append(int(part))
        except ValueError:
            # ignore invalid values rather than crashing
            pass
    return items


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: list[int]
    db_path: str
    log_level: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing. Put it in .env or environment variables.")

    admin_ids = _split_ints(os.getenv("ADMIN_IDS", ""))
    db_path = os.getenv("DB_PATH", "bot.sqlite3").strip() or "bot.sqlite3"
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"

    return Config(
        bot_token=bot_token,
        admin_ids=admin_ids,
        db_path=db_path,
        log_level=log_level,
    )
