from dataclasses import dataclass
from typing import Optional
from typing import TypedDict
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

# NOTE it'll create __init__ method automatically
@dataclass
class VolcanoUser():
    id: Optional[int]
    user_id: Optional[UUID] # is it type UUID?
    username: str
    hashed_password: str
    email: str
    icon: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]