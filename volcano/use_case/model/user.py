from pydantic import BaseModel, Field
from typing import Optional


class UpdateUserModel(BaseModel):
    email: Optional[str] = Field(min_length=3)
    username: Optional[str]
    icon: Optional[str]
