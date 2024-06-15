from dataclasses import dataclass
from typing import Optional
from typing import TypedDict
from datetime import datetime
import uuid


@dataclass
class Todo:
    id: Optional[int] = None
    todo_id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    period: Optional[datetime] = None
    priority: int = 1
    type: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    audio_url: Optional[str] = None
    is_completed: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None