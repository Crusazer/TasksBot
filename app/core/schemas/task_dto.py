import dataclasses
import uuid
from datetime import datetime


@dataclasses.dataclass
class TaskDTO:
    id: uuid.UUID
    user_id: str
    name: str
    description: str
    status: bool
    deadline: datetime
    created_at: datetime


@dataclasses.dataclass
class CreateTaskDTO:
    user_id: str
    name: str
    description: str
    status: bool
    deadline: datetime
    created_at: datetime


@dataclasses.dataclass
class UpdateTaskDTO:
    id: uuid.UUID
    description: str | None
    status: bool | None
    deadline: datetime | None
