from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: list[int]
    db_path: str
    log_level: str


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN missing")

    admins = [
        int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
    ]

    return Config(
        bot_token=token,
        admin_ids=admins,
        db_path=os.getenv("DB_PATH", "bot.sqlite3"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
