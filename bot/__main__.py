from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from .config import load_config
from .db import Database
from .handlers import (
    about,
    broadcast,
    echo_text,
    error_handler,
    help_cmd,
    ping,
    start,
    stats,
)
from .logging_setup import setup_logging


async def main() -> None:
    # Load .env if present (works in local dev)
    load_dotenv()

    cfg = load_config()
    setup_logging(cfg.log_level)

    db = Database(cfg.db_path)

    app = (
        Application.builder()
        .token(cfg.bot_token)
        .build()
    )

    # shared objects
    app.bot_data["cfg"] = cfg
    app.bot_data["db"] = db

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("about", about))

    # admin
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))

    # errors
    app.add_error_handler(error_handler)

    # run
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=[])
    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        db.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
