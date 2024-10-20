import abc
import logging
from typing import Iterable

import aiosqlite
from aiosqlite import Cursor, Row

from core.schemas.task_dto import TaskDTO, UpdateTaskDTO, CreateTaskDTO
from config import settings
from . import row_sql_query

logger = logging.getLogger(__name__)


class TaskRepository(abc.ABC):
    """
        Abstract class for working with tasks in any database. Used in business logic.
        If you need to change the ORM or database, you should implement this class.
    """

    @abc.abstractmethod
    async def create(self, task: CreateTaskDTO) -> TaskDTO:
        pass

    @abc.abstractmethod
    async def get_by_id(self, task_id: int) -> TaskDTO:
        pass

    @abc.abstractmethod
    async def get_all(self, user_id: str) -> list[TaskDTO]:
        pass

    @abc.abstractmethod
    async def update(self, task: UpdateTaskDTO):
        pass

    @abc.abstractmethod
    async def delete(self, task_id: int):
        pass


class SqLiteTaskRepository(TaskRepository):
    async def create(self, task: CreateTaskDTO) -> TaskDTO:
        """
        Create a mew task and return DTO the new task.
        Make 2 execute to database for create new task and get info about this task.
        """
        async with aiosqlite.connect(settings.DB_NAME) as connection:
            # Create new task
            cursor: Cursor = await connection.execute(
                row_sql_query.CREATE_TASK,
                (task.user_id, task.description, int(task.status), task.deadline)
            )
            await connection.commit()

            # Get task data from db
            task_id: int = cursor.lastrowid
            cursor: Cursor = await connection.execute(row_sql_query.GET_TASK_BY_ID, (task_id,))
            data: Row = await cursor.fetchone()
            return TaskDTO(*data)

    async def get_by_id(self, task_id: int) -> TaskDTO:
        """
        Get a mew task by id.
        Make 1 execute to database for get info about this task.
        """
        async with aiosqlite.connect(settings.DB_NAME) as connection:
            cursor: Cursor = await connection.execute(row_sql_query.GET_TASK_BY_ID, (task_id,))
            data: Row = await cursor.fetchone()
            return TaskDTO(*data)

    async def get_all(self, user_id: str) -> list[TaskDTO]:
        """
        Get all user tasks by user id from database.
        Make 1 execute to database for get info about user tasks.
        """
        async with aiosqlite.connect(settings.DB_NAME) as connection:
            cursor: Cursor = await connection.execute(row_sql_query.GET_TASKS_BY_USER_ID, (user_id,))
            tasks_data: Iterable[Row] = await cursor.fetchall()
            return [TaskDTO(*data) for data in tasks_data]

    async def update(self, task: UpdateTaskDTO):
        """
        Update a task by id.
        Make one execute to the databaseUpdate for change description, status or deadline of task by task id.
        """
        async with aiosqlite.connect(settings.DB_NAME) as connection:
            await connection.execute(
                row_sql_query.UPDATE_TASK_BY_ID,
                (task.description, task.status, task.deadline, task.id)
            )
            await connection.commit()

    async def delete(self, task_id: int):
        """
        Delete a task by id.
        Make one execute to database for delete a task.
        """
        async with aiosqlite.connect(settings.DB_NAME) as connection:
            await connection.execute(row_sql_query.DELETE_TASK_BY_ID, (task_id,))
            await connection.commit()
