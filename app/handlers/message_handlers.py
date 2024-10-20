import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.repository.task_repository import SQLiteTaskRepository
from core.schemas.task_dto import TaskDTO
from core.services.task_service import TaskService
from keyboards import inline_task_keyboard
from .create_task_handlers import CreateTaskSteps

logger = logging.getLogger(__name__)


async def create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Start conversation to create new task."""
    await update.message.reply_text("Введите новое описание для задачи (для отмены введите /cancel): ")
    logger.info("User %s start creating new task", update.message.from_user.id)
    return CreateTaskSteps.DESCRIPTION


async def all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Send to the user all his tasks"""
    # Get all tasks by telegram user id
    user_id: int = update.message.from_user.id
    task_service: TaskService = TaskService(SQLiteTaskRepository())
    tasks: list[TaskDTO] = await task_service.get_all_tasks(user_id)

    # Send tasks messages to user
    for task in tasks:
        text_message = (f"{task.description}\n"
                        f"<b>Срок выполнения:</b> {task.deadline}\n"
                        f"<b>Статус:</b> {'✅' if task.status else '❌'}\n"
                        f"<b>Изменена:</b> {task.updated_at}\n"
                        f"<b>Создана:</b> {task.created_at}"
                        )
        await update.message.reply_text(
            text_message,
            parse_mode=ParseMode.HTML,
            reply_markup=inline_task_keyboard(task.id)
        )

    logger.info("User %s get all tasks", user_id)
