from fastapi import APIRouter, Depends
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....infrastructure.postgresql.dto.volcano_user_dto import VolcanoUserDTO



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]