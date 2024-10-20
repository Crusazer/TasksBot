import uuid

from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO
from core.repository.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task: CreateTaskDTO) -> TaskDTO:
        """ Creates a new task in the database. """
        created_task: TaskDTO = await self.task_repository.create(task)
        return created_task

    async def get_all_tasks(self, user_id: str):
        """ Returns a list of all tasks from the database.
        :param user_id: user id from telegram.
        """
        tasks: list[TaskDTO] = await self.task_repository.get_all(user_id)
        return tasks

    async def update_task(self, task: UpdateTaskDTO):
        """ Updates a task status/description/deadline in the database. """
        task: TaskDTO = await self.task_repository.update(task)
        return task

    async def delete_task(self, task_id: uuid.UUID):
        """ Deletes a task in the database. """
        await self.task_repository.delete(task_id)
