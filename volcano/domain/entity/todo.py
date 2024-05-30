from dataclasses import dataclass
from typing import Optional
from typing import TypedDict
from datetime import datetime
import uuid


@dataclass
class Todo:
    id: Optional[int]
    todo_id: Optional[uuid.UUID]
    title: str
    description: Optional[str]
    period: datetime
    priority: int
    type: Optional[str]
    user_id: uuid.UUID
    audio_url: str
    is_completed: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]