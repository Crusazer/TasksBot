import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards.keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Вы можете управлять своими задачами с помощью этого бота.",
                                    reply_markup=main_menu_keyboard())
    logger.info('New user %s start to use the bot', update.message.from_user.id)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Processing dialog cancellation. """
    await update.message.reply_text("Операция отменена.")
    logger.info("User %s canceled create or update task.", update.message.from_user.id)
    return ConversationHandler.END
