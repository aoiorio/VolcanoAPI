from dataclasses import dataclass
from typing import Optional
from typing import TypedDict
from datetime import datetime
import uuid

# NOTE it'll create __init__ method automatically
@dataclass
class VolcanoUser:
    id: Optional[int] = None
    user_id: Optional[uuid.UUID] = None
    username: Optional[str] = None
    hashed_password: str = ""
    email: str = ""
    icon: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None