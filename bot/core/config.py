from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: list[int]
    log_level: str
    database_url: str


def load_config() -> Config:
    token = (os.getenv("BOT_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN missing")

    admin_ids = []
    for x in (os.getenv("ADMIN_IDS") or "").split(","):
        x = x.strip()
        if x.isdigit():
            admin_ids.append(int(x))

    db_url = (os.getenv("DATABASE_URL") or "").strip()
    if not db_url:
        raise RuntimeError("DATABASE_URL missing")

    log_level = (os.getenv("LOG_LEVEL") or "INFO").strip().upper()

    return Config(
        bot_token=token,
        admin_ids=admin_ids,
        log_level=log_level,
        database_url=db_url,
    )
