import os
from datetime import datetime

import aiosqlite
import pytest

from app.core.repository.task_repository import SQLiteTaskRepository
from app.core.schemas.task_dto import CreateTaskDTO
from config import settings
from core.repository.row_sql_query import CREATE_TASK_TABLE, CREATE_AUTO_AUTOUPDATE_TIMESTAMP


@pytest.fixture(scope="module", autouse=False)
async def setup_test_db():
    test_db_name = "test.db"
    original_db_name = settings.DB_NAME
    settings.DB_NAME = test_db_name

    async with aiosqlite.connect(test_db_name) as db:
        await db.execute(CREATE_TASK_TABLE)
        await db.execute(CREATE_AUTO_AUTOUPDATE_TIMESTAMP)
        await db.commit()

    yield

    if os.path.exists(test_db_name):
        os.remove(test_db_name)

    settings.DB_NAME = original_db_name


@pytest.fixture
async def test_task():
    repository = SQLiteTaskRepository()
    task_data = CreateTaskDTO(
        user_id=123,
        description="Test task",
        status=False,
        deadline=datetime(9000, 1, 1))
    task = await repository.create(task_data)
    yield task
    await repository.delete(task.id)
