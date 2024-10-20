import dataclasses
from datetime import datetime


@dataclasses.dataclass
class TaskDTO:
    """ Used to transfer task data in business logic. """
    id: int
    user_id: str
    description: str
    status: bool
    deadline: datetime | str
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass
class CreateTaskDTO:
    """ Used to create a new task """
    user_id: int
    description: str
    status: bool
    deadline: datetime


@dataclasses.dataclass
class UpdateTaskDTO:
    """ Used to update a task """
    id: int
    description: str
    deadline: datetime
