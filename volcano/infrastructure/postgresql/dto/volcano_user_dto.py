# NOTE This file is for creating a table called volcano_user
# NOTE DTO stands for Data Transfer Object
from sqlalchemy import text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import BaseModel
from ....domain.entity.user import VolcanoUser

import uuid
from datetime import datetime


class VolcanoUserDTO(BaseModel):
    __tablename__ = "volcano_user"
    __table_args__ = {"comment": "This is volcano_user master table"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # NOTE Generate uuid as default value
    # ! you must add unique=True field for migrating Foreign Key from other tables!!!!
    # NOTE server_default can insert default sentence in postgres command when I create a table
    user_id: Mapped[uuid.UUID] = mapped_column(
        server_default=text("uuid_generate_v4()"),
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    icon: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(),)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), onupdate=func.now(),)

    # NOTE This method is for combining to entity called VolcanoUser
    def to_entity(self) -> VolcanoUser:
        return VolcanoUser(
            id=self.id,
            user_id=self.user_id,
            username=self.username,
            hashed_password=self.hashed_password,
            icon=self.icon,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    # NOTE staticmethod is for using this method from_entity without initializing like VolcanoUserDTO.from_entity(), and it never changes from other functions or methods
    @staticmethod
    def from_entity(volcano_user: VolcanoUser) -> "VolcanoUserDTO":
        return VolcanoUserDTO(
            id=volcano_user.id,
            user_id=volcano_user.user_id,
            username=volcano_user.username,
            hashed_password=volcano_user.hashed_password,
            icon=volcano_user.icon,
            created_at=volcano_user.created_at,
            updated_at=volcano_user.updated_at,
        )
