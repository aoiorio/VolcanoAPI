# NOTE This file is for creating a table called todo

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# from .volcano_user_dto import VolcanoUserDTO
from ..database import BaseModel
# from uuid import uuid4

class TodoDTO(BaseModel):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    todo_id = Column(
        UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(String)
    period = Column(DateTime, nullable=False)
    priority = Column(Integer, default=1, server_default=text("1"),)
    type = Column(String)
    # NOTE It's related to user id
    user_id = Column(
        'user_id',
        UUID(as_uuid=True),
        ForeignKey('volcano_user.user_id', ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    audio_url = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False, server_default=text("FALSE"),)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
    )