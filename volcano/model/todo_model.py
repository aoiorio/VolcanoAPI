from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .volcano_user_model import VolcanoUser
from .base_model import BaseModel
from uuid import uuid4

class Todo(BaseModel):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    todo_id = Column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(String)
    period = Column(DateTime, nullable=False)
    priority = Column(Integer, default=1)
    type = Column(String)
    # NOTE It's related to user id
    user_id = Column(
        'user_id',
        UUID(as_uuid=True),
        ForeignKey('volcano_user.user_id', ondelete="CASCADE"),
        nullable=False,
    )
    audio_url = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )