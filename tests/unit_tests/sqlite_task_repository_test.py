import logging
from datetime import datetime

import pytest

from app.core.repository.task_repository import SQLiteTaskRepository
from app.core.schemas.task_dto import CreateTaskDTO, TaskDTO, UpdateTaskDTO

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("setup_test_db")
class TestSQLiteTaskRepository:
    @pytest.mark.asyncio
    async def test_create_task(self):
        repository = SQLiteTaskRepository()
        task_data = CreateTaskDTO(user_id=1,
                                  description="Test task",
                                  status=False,
                                  deadline=datetime(3100, 10, 21, 18, 00, 00))
        task: TaskDTO = await repository.create(task_data)
        assert task.user_id == task_data.user_id
        assert task.description == task_data.description
        assert task.status == 0

    async def test_get_task(self, test_task: TaskDTO):
        repository = SQLiteTaskRepository()
        task: TaskDTO = await repository.get_by_id(test_task.id)

        assert task.id == test_task.id
        assert task.user_id == test_task.user_id
        assert task.description == test_task.description
        assert task.status == test_task.status
        assert task.deadline == test_task.deadline
        assert task.created_at == test_task.created_at
        assert task.updated_at == test_task.updated_at

    async def test_get_all_tasks(self):
        repository = SQLiteTaskRepository()
        tasks: list = await repository.get_all(10)
        assert len(tasks) == 0

        task_data = CreateTaskDTO(
            user_id=10,
            description="Test task",
            status=False,
            deadline=datetime(9000, 1, 1))
        await repository.create(task_data)
        task_data.user_id = 10
        await repository.create(task_data)

        tasks: list[TaskDTO] = await repository.get_all(10)
        assert len(tasks) == 2

    async def test_update_task(self, test_task: TaskDTO):
        repository = SQLiteTaskRepository()
        update_task: UpdateTaskDTO = UpdateTaskDTO(
            id=test_task.id,
            description="update test",
            deadline=datetime(9999, 10, 21, 18, 00, 00)
        )
        updated_task = await repository.update(update_task)
        assert updated_task.description == update_task.description
        assert updated_task.deadline == update_task.deadline.strftime('%Y-%m-%d %H:%M:%S')

    async def test_complete_task(self, test_task: TaskDTO):
        repository = SQLiteTaskRepository()
        await repository.complete(test_task.id)
        task: TaskDTO = await repository.get_by_id(test_task.id)
        assert task.id == test_task.id
        assert task.status == 1

    async def test_delete_task(self, test_task: TaskDTO):
        repository = SQLiteTaskRepository()
        await repository.delete(test_task.id)
        task: TaskDTO = await repository.get_by_id(test_task.id)
        assert task is None

