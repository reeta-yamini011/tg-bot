from telegram import Update
from telegram.ext import ContextTypes
from bot.database.queries import total_users


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
