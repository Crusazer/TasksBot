import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config import settings
from utils import prepare_database

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Вы можете управлять своими задачами с помощью этого бота.")


if __name__ == '__main__':
    prepare_database()
    app = ApplicationBuilder().token(settings.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
