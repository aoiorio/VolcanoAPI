# NOTE This file is for creating a table called todo

from sqlalchemy import ForeignKey, text
# from sqlalchemy import text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime
from ....domain.entity.todo import Todo
from ..database import BaseModel


class TodoDTO(BaseModel):
    __tablename__ = "todo"
    __table_args__ = {"comment": "This is todo master table"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    todo_id: Mapped[uuid.UUID] = mapped_column(
        server_default=text("uuid_generate_v4()"),
        primary_key=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    period: Mapped[datetime] = mapped_column(nullable=False)
    priority: Mapped[int] = mapped_column(
        default=1,
        server_default=text("1"),
    )
    type: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("volcano_user.user_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    audio_url: Mapped[str] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("FALSE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )

    # NOTE This method is for combining to entity called VolcanoUser
    def to_entity(self) -> Todo:
        return Todo(
            id=self.id,
            todo_id=self.todo_id,
            title=self.title,
            description=self.description,
            period=self.period,
            priority=self.priority,
            type=self.type,
            user_id=self.user_id,
            audio_url=self.audio_url,
            is_completed=self.is_completed,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    # NOTE staticmethod is for using this method from_entity without initializing like VolcanoUserDTO.from_entity(), and it never changes from other functions or methods
    @staticmethod
    def from_entity(todo: Todo) -> "TodoDTO":
        return TodoDTO(
            id=todo.id,
            todo_id=todo.todo_id,
            title=todo.title,
            description=todo.description,
            period=todo.period,
            priority=todo.priority,
            type=todo.type,
            user_id=todo.user_id,
            audio_url=todo.audio_url,
            is_completed=todo.is_completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
