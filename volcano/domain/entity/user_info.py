from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class UserInfo:
    user_id: Optional[uuid.UUID] = None
    username: Optional[str] = None
    email: str = ""
    icon: Optional[str] = None
    done_todo_num: Optional[int] = None
    not_yet_todo_num: Optional[int] = None
