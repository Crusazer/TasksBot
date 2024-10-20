import logging

from telegram import Update
from telegram.ext import ContextTypes, Updater

from core.repository.task_repository import SQLiteTaskRepository
from core.services.task_service import TaskService
from .update_task_handlers import UpdateTaskSteps
from config import settings

logger = logging.getLogger(__name__)


async def update_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ This callback handler used to change description and deadline of task. """
    query = update.callback_query
    await query.answer()

    task_id = int(query.data.split("_")[1])
    context.user_data['task_id'] = task_id
    await query.edit_message_text("Введите новое описание для задачи (для отмены введите /cancel):")
    logger.info("User start to update task %s", task_id)
    return UpdateTaskSteps.DESCRIPTION


async def complete_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ This callback handler used to change task status to complete by task id from callback data."""
    query = update.callback_query
    await query.answer()

    task_id = int(query.data.split("_")[1])
    task_service = TaskService(SQLiteTaskRepository())
    await task_service.complete_task(task_id)
    await query.edit_message_text("Задача завершена!")
    logger.info("User complete task %s", task_id)


async def delete_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ This callback handler used to delete a task fom database based on task id from callback data."""
    query = update.callback_query
    await query.answer()

    task_id = int(query.data.split("_")[1])
    task_service = TaskService(SQLiteTaskRepository())
    await task_service.delete_task(task_id)
    await query.edit_message_text("Задача удалена успешно!")
    logger.info("User deleted task %s", task_id)
