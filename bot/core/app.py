import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from bot.core.config import load_config
from bot.core.logging import setup_logging
from bot.database.connection import Database
from bot.handlers import common, admin, messages
from bot.handlers.errors import error_handler
from bot.middlewares.user_tracker import track_user


async def run_app():
    load_dotenv()
    cfg = load_config()
    setup_logging(cfg.log_level)

    db = Database(cfg.db_path)

    app = Application.builder().token(cfg.bot_token).build()
    app.bot_data["config"] = cfg
    app.bot_data["db"] = db

    # middleware
    app.add_handler(MessageHandler(filters.ALL, track_user), group=0)

    # commands
    app.add_handler(CommandHandler("start", common.start))
    app.add_handler(CommandHandler("help", common.help_cmd))
    app.add_handler(CommandHandler("ping", common.ping))
    app.add_handler(CommandHandler("about", common.about))

    # admin
    app.add_handler(CommandHandler("stats", admin.stats))
    app.add_handler(CommandHandler("broadcast", admin.broadcast))
    app.add_handler(CommandHandler("broadcast_copy", admin.broadcast_copy_cmd))
    # messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages.echo))

    app.add_error_handler(error_handler)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()
