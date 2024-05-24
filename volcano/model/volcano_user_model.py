from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .base_model import BaseModel
from uuid import uuid4


class VolcanoUser(BaseModel):
    __tablename__ = 'volcano_user'
    __table_args__ = {
        'comment': 'This is user master table'
    }

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    # NOTE Generate uuid as default value
    # ! you must add unique=True field for migrating Foreign Key from other tables!!!!
    user_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False, unique=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    icon = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())