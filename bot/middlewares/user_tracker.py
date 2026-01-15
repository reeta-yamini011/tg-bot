from telegram import Update
from telegram.ext import ContextTypes
from bot.database.queries import upsert_user


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return

    user = update.effective_user
    db = context.bot_data["db"]

    full_name = " ".join(filter(None, [user.first_name, user.last_name]))
    upsert_user(db, user.id, user.username, full_name)
