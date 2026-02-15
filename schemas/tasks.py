from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class TaskStatus(StrEnum):
    INBOX = 'inbox'
    PLANNED = 'planned'
    DONE = 'done'


class TaskItem(BaseModel):
    id: int
    text: str
    status: TaskStatus
    created_at: datetime
    priority: str | None
    category: str | None
    estimated_minutes: int | None
    ai_analyzed: datetime | None