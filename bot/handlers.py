from __future__ import annotations

import logging
from typing import Iterable

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .db import Database

log = logging.getLogger("bot.handlers")


def _is_admin(user_id: int | None, admin_ids: Iterable[int]) -> bool:
    return user_id is not None and user_id in set(admin_ids)


async def _track_user(update: Update, db: Database) -> None:
    if not update.effective_user:
        return
    u = update.effective_user
    full_name = " ".join(x for x in [u.first_name, u.last_name] if x) or None
    db.upsert_user(user_id=u.id, username=u.username, full_name=full_name)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    name = update.effective_user.first_name if update.effective_user else "there"
    text = (
        f"Hey {name}! 👋\n\n"
        "I’m alive and working.\n\n"
        "Try:\n"
        "• /help\n"
        "• /ping\n"
    )
    await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    cfg = context.bot_data["cfg"]
    admin_help = ""
    if _is_admin(update.effective_user.id if update.effective_user else None, cfg.admin_ids):
        admin_help = (
            "\n\n*Admin commands:*\n"
            "• /stats — total users\n"
            "• /broadcast <message> — send message to everyone (safe: limited info)\n"
        )

    text = (
        "*Commands*\n"
        "• /start — welcome\n"
        "• /help — this menu\n"
        "• /ping — health check\n"
        "• /about — what this is\n"
        f"{admin_help}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)
    await update.message.reply_text("pong ✅")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    await update.message.reply_text(
        "A minimal Telegram bot template 🤖\n"
        "Built with python-telegram-bot (async), SQLite user tracking, and admin tools."
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    cfg = context.bot_data["cfg"]
    if not _is_admin(update.effective_user.id if update.effective_user else None, cfg.admin_ids):
        await update.message.reply_text("⛔ Not allowed.")
        return

    total = db.total_users()
    await update.message.reply_text(f"📊 Total users: {total}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Admin-only broadcast.
    NOTE: For simplicity, this template does not store chat IDs separately.
    If you want true broadcast to all chats, we should store user chat_id (private) on /start.
    """
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    cfg = context.bot_data["cfg"]
    if not _is_admin(update.effective_user.id if update.effective_user else None, cfg.admin_ids):
        await update.message.reply_text("⛔ Not allowed.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    # This template keeps broadcast intentionally safe & simple:
    # It broadcasts only back to the current chat (so it “works” without extra tables),
    # and you can upgrade it to real broadcast by storing chat_ids.
    msg = " ".join(context.args).strip()
    await update.message.reply_text(f"📣 Broadcast preview (this chat only):\n\n{msg}")


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db: Database = context.bot_data["db"]
    await _track_user(update, db)

    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    # ignore commands
    if text.startswith("/"):
        return

    await update.message.reply_text(text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("Unhandled error: %s", context.error)
