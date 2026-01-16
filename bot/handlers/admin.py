from telegram import Update
from telegram.ext import ContextTypes
from bot.database.queries import total_users
from bot.services.broadcaster import broadcast_text, broadcast_copy

def is_admin(update, context):
    return update.effective_user.id in context.bot_data["config"].admin_ids


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update, context):
        await update.message.reply_text("⛔ Not allowed")
        return

    count = total_users(context.bot_data["db"])
    await update.message.reply_text(f"👥 Users: {count}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update, context):
        await update.message.reply_text("⛔ Not allowed")
        return

    msg = " ".join(context.args)
    await update.message.reply_text(f"📣 Broadcast preview:\n\n{msg}")

async def broadcast_copy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update, context):
        await update.message.reply_text("⛔ Not allowed")
        return

    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text(
            "Usage: Reply to ANY message (photo/video/document/text/etc) and run:\n"
            "/broadcast_copy"
        )
        return

    await update.message.reply_text("📣 Broadcasting media/message to all users…")

    app = context.application
    sessionmaker = context.bot_data["sessionmaker"]

    src_chat_id = update.effective_chat.id
    src_message_id = update.message.reply_to_message.message_id

    result = await broadcast_copy(
        app,
        sessionmaker,
        from_chat_id=src_chat_id,
        message_id=src_message_id,
    )

    await update.message.reply_text(
        f"✅ Broadcast done\n"
        f"Total: {result.total}\n"
        f"Sent: {result.sent}\n"
        f"Blocked: {result.blocked}\n"
        f"Failed: {result.failed}"
    )
