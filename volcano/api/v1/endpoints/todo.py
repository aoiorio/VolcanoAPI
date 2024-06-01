from fastapi import APIRouter, Depends
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....infrastructure.postgresql.dto.todo_dto import TodoDTO
from fastapi.security import OAuth2PasswordBearer



router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todo/")
async def read_all_todos(db: db_dependency, token: str =  Depends(oauth2_scheme)):
    return db.query(TodoDTO).all()

