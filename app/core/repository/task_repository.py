import abc
import uuid

from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO


class TaskRepository(abc):
    """
        Abstract class for working with tasks in any database. Used in business logic.
        If you need to change the ORM or database, you should implement this class.
    """

    @abc.abstractmethod
    async def create(self, task: CreateTaskDTO) -> TaskDTO:
        pass

    @abc.abstractmethod
    async def get_by_id(self, task_id: uuid.UUID) -> TaskDTO:
        pass

    @abc.abstractmethod
    async def get_all(self, user_id: str) -> list[TaskDTO]:
        pass

    @abc.abstractmethod
    async def update(self, task: UpdateTaskDTO):
        pass

    @abc.abstractmethod
    async def delete(self, task_id: uuid.UUID):
        pass


class SqLiteTaskRepository(TaskRepository):
    pass
