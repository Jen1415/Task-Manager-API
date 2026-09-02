from datetime import datetime
from pydantic import BaseModel, ConfigDict
from taskmanagerapi.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime
    status: TaskStatus = TaskStatus.todo

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    status: TaskStatus | None = None

class TaskResponse(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)