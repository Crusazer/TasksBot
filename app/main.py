from time import sleep

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Вы можете управлять своими задачами с помощью этого бота.")
    print(context)


if __name__ == '__main__':
    app = ApplicationBuilder().token(settings.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
