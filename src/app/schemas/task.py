import uuid
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, conint

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None
    priority: Annotated[int, conint(ge=1, le=5)] = 3  # 1=Low, 2=Medium, 3=Normal, 4=High, 5=Top
    due_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: Annotated[int, conint(ge=1, le=5)]
    due_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

class TaskOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None = None
    status: str | None = None
    priority: Annotated[int, conint(ge=1, le=5)]
    due_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)