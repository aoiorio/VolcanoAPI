from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TodoPostModel(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str]
    period: datetime
    type: str = Field(min_length=2)
    priority: int = Field(ge=1, le=5)


class TodoUpdateModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    period: Optional[datetime]
    type: Optional[str] = "others"
    priority: Optional[int] = 3
    is_completed: Optional[bool] = False
    audio_url: Optional[str]
