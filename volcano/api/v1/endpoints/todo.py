from fastapi import APIRouter, Depends
from ....core.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....model.todo_model import Todo



router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def read_all_todos(db: db_dependency):
    return db.query(Todo).all()

