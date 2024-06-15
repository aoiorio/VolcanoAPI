from pydantic import BaseModel, Field
from datetime import datetime

# class TodoPostModel(BaseModel):
#     title: str = Field(min_length=3)
#     description: str
#     period: datetime = Field(min_length=4)
#     type: str = Field(min_length=2)
#     # audio: str = Field(min_length=10)
#     priority: int = Field(ge=1, le=5)