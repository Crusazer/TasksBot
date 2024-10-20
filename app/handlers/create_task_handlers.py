import enum
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from core.schemas.task_dto import TaskDTO
from managers.task_manager import TaskManager

logger = logging.getLogger(__name__)


class CreateTasksSteps(enum.Enum):
    DESCRIPTION = 2
    DEADLINE = 3


async def handle_create_task_description(update: Update, context: CallbackContext):
    """ Get description task from user message and save it in user context. """
    await TaskManager.get_description_from_user_message(update, context)
    return CreateTasksSteps.DEADLINE


async def handle_create_task_deadline(update: Update, context: CallbackContext):
    """ Get deadline of task from user message and create new task """
    deadline: datetime = await TaskManager.get_deadline(update)
    if deadline is None:
        return CreateTasksSteps.DEADLINE
    task: TaskDTO = await TaskManager.create_task(update, context, deadline)
    logger.info("User %s created new task %s", update.message.from_user.id, task.id)
