import time


def upsert_user(db, user_id, username, full_name):
    now = int(time.time())
    db.conn.execute("""
    INSERT INTO users VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        username=excluded.username,
        full_name=excluded.full_name,
        last_seen=excluded.last_seen
    """, (user_id, username, full_name, now, now))
    db.conn.commit()


def total_users(db):
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]
