from datetime import datetime
from enum import StrEnum
from schemas.base_schemas import SchemaBase


class TaskStatus(StrEnum):
    INBOX = 'inbox'
    PLANNED = 'planned'
    DONE = 'done'


class TaskItem(SchemaBase):
    id: int
    text: str
    status: TaskStatus
    created_at: datetime
    priority: str | None
    category: str | None
    estimated_minutes: int | None
    ai_analyzed: datetime | None