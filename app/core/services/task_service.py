import uuid

from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO
from core.repository.task_repository import TaskRepository


class TaskService:
    @staticmethod
    async def create_task(task: CreateTaskDTO) -> TaskDTO:
        """ Creates a new task in the database. """
        repository: TaskRepository = TaskRepository()
        created_task: TaskDTO = await repository.create(task)
        return created_task

    @staticmethod
    async def get_all_tasks(user_id: str):
        """ Returns a list of all tasks from the database.
        :param user_id: user id from telegram.
        """
        repository: TaskRepository = TaskRepository()
        tasks: list[TaskDTO] = await repository.get_all(user_id)
        return tasks

    @staticmethod
    async def update_task(task: UpdateTaskDTO):
        """ Updates a task status/description/deadline in the database. """
        repository: TaskRepository = TaskRepository()
        task: TaskDTO = await repository.update(task)
        return task

    @staticmethod
    async def delete_task(task_id: uuid.UUID):
        """ Deletes a task in the database. """
        repository: TaskRepository = TaskRepository()
        await repository.delete(task_id)
