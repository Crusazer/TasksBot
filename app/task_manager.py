from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from core.repository.task_repository import SQLiteTaskRepository
from core.schemas.task_dto import UpdateTaskDTO, CreateTaskDTO, TaskDTO
from core.services.task_service import TaskService


class TaskManager:
    @staticmethod
    async def get_description_from_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        new_description = update.message.text
        context.user_data['description'] = new_description
        await update.message.reply_text("Введите срок выполнения задачи в формате 'ГГГГ ММ ДД ЧЧ мм': ")

    @staticmethod
    async def get_deadline(update: Update) -> datetime | None:
        new_deadline_str: str = update.message.text
        try:
            deadline = datetime.strptime(new_deadline_str, "%Y %m %d %H %M")
            if datetime.now() > deadline:
                await update.message.reply_text("Срок выполнения не может быть раньше, чем сегодня. "
                                                "Введите корректную дату")
                return None
            return deadline
        except ValueError:
            await update.message.reply_text("Неверный формат даты. Попробуйте еще раз (в формате ГГГГ-ММ-ДД).")
            return None

    @staticmethod
    async def update_task(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            new_deadline: datetime,
    ):
        task_service = TaskService(SQLiteTaskRepository())

        task_id: int = context.user_data['task_id']
        description: str = context.user_data['description']
        task = UpdateTaskDTO(task_id, description, new_deadline)
        await task_service.update_task(task)
        await update.message.reply_text("Задача успешно обновлена!")

    @staticmethod
    async def create_task(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            deadline: datetime
    ) -> TaskDTO:
        """ Create new task. """
        task_service = TaskService(SQLiteTaskRepository())
        description: str = context.user_data['description']
        create_task_dto = CreateTaskDTO(
            user_id=update.message.from_user.id,
            description=description,
            status=False,
            deadline=deadline
        )
        task: TaskDTO = await task_service.create_task(create_task_dto)
        await update.message.reply_text("Задача успешно создана.")
        return task
