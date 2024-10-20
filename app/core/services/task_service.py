from core.repository.task_repository import TaskRepository
from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO
from utils import convert_time_to_local, convert_time_to_utc


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task: CreateTaskDTO) -> TaskDTO:
        """ Convert deadline time to UTC format and creates a new task in the database.  """
        task.deadline = convert_time_to_utc(task.deadline)
        created_task: TaskDTO = await self.task_repository.create(task)
        return created_task

    async def get_all_tasks(self, user_id: int) -> list[TaskDTO]:
        """ Returns a list of all tasks from the database. Converted all time to local. """
        tasks: list[TaskDTO] = await self.task_repository.get_all(user_id)
        for task in tasks:
            task.deadline = convert_time_to_local(task.deadline)
            task.created_at = convert_time_to_local(task.created_at)
            task.updated_at = convert_time_to_local(task.updated_at)
        return tasks

    async def complete_task(self, task_id: int):
        """ Updates a task status/description/deadline in the database. """
        await self.task_repository.complete(task_id)

    async def update_task(self, task: UpdateTaskDTO):
        """ Updates a task status/description/deadline in the database. """
        task.deadline = convert_time_to_utc(task.deadline)
        return await self.task_repository.update(task)

    async def delete_task(self, task_id: int):
        """ Deletes a task in the database. """
        await self.task_repository.delete(task_id)
