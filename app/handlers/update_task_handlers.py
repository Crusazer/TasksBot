import enum
import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from managers.task_manager import TaskManager

logger = logging.getLogger(__name__)


class UpdateTasksSteps(enum.Enum):
    DESCRIPTION = 0
    DEADLINE = 1


async def handle_update_task_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Get new task description from user message"""
    await TaskManager.get_description_from_user_message(update, context)
    return UpdateTasksSteps.DEADLINE


async def handle_update_task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Get new task deadline from user """
    deadline = await TaskManager.get_deadline(update)
    # If user send incorrect data
    if deadline is None:
        return UpdateTasksSteps.DEADLINE

    await TaskManager.update_task(update, context, deadline)
    logger.info("User %s update task %s", update.message.chat.id, context.user_data['task_id'])
    return ConversationHandler.END
