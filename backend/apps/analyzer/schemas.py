from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'


class TaskResult(BaseModel):
    table_img: str
    type: str


class TaskSchema(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[list[TaskResult]] = None
