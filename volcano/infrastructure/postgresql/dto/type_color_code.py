from sqlalchemy import text

from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime

from volcano.domain.entity.type_color_code import TypeColorCode
from ..database import BaseModel


class TypeColorCodeDTO(BaseModel):
    __tablename__ = "type_color_code"
    __table_args__ = {"comment": "This is type_color_code master table, it can contain hex color codes"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    color_id: Mapped[uuid.UUID] = mapped_column(
        server_default=text("uuid_generate_v4()"),
        primary_key=True,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    start_color_code: Mapped[str] = mapped_column(
        nullable=False,
    )
    end_color_code: Mapped[str] = mapped_column(
        nullable=False
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
    def to_entity(self) -> TypeColorCode:
        return TypeColorCode(
            id=self.id,
            color_id=self.color_id,
            type=self.type,
            start_color_code=self.start_color_code,
            end_color_code=self.end_color_code,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    # NOTE staticmethod is for using this method from_entity without initializing like VolcanoUserDTO.from_entity(), and it never changes from other functions or methods
    @staticmethod
    def from_entity(type_color_object: TypeColorCode) -> "TypeColorCodeDTO":
        return TypeColorCodeDTO(
            id=type_color_object.id,
            color_id=type_color_object.color_id,
            type=type_color_object.type,
            start_color_code=type_color_object.start_color_code,
            end_color_code=type_color_object.end_color_code,
            created_at=type_color_object.created_at,
            updated_at=type_color_object.updated_at,
        )
