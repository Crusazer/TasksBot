from core.repository.task_repository import TaskRepository
from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task: CreateTaskDTO) -> TaskDTO:
        """ Creates a new task in the database. """
        created_task: TaskDTO = await self.task_repository.create(task)
        return created_task

    async def get_all_tasks(self, user_id: int) -> list[TaskDTO]:
        """ Returns a list of all tasks from the database.
        """
        tasks: list[TaskDTO] = await self.task_repository.get_all(user_id)
        return tasks

    async def complete_task(self, task_id: int):
        """ Updates a task status/description/deadline in the database. """
        await self.task_repository.complete(task_id)

    async def update_task(self, task: UpdateTaskDTO):
        """ Updates a task status/description/deadline in the database. """
        await self.task_repository.update(task)

    async def delete_task(self, task_id: int):
        """ Deletes a task in the database. """
        await self.task_repository.delete(task_id)
