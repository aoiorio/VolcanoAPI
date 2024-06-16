from fastapi import APIRouter, Depends, UploadFile
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ....use_case.todo.todo_use_case import TodoUseCase, TodoUseCaseImpl
from ....infrastructure.repository.todo.todo_repository_impl import TodoRepository, TodoRepositoryImpl
from ....infrastructure.repository.auth.auth_repository_impl import (
    AuthRepository,
    AuthRepositoryImpl,
)


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


def todo_use_case(db: Session = Depends(get_db)) -> TodoUseCase:
    """Get a book command use case."""
    # NOTE ここでrepositoryをrepositoryImplにしている
    todo_repository: TodoRepository = TodoRepositoryImpl(db=db)
    auth_repository: AuthRepository = AuthRepositoryImpl(db=db)
    return TodoUseCaseImpl(todo_repository, auth_repository)


@router.post("/")
async def post_todo(audio: UploadFile, token: str, todo_use_case: TodoUseCase = Depends(todo_use_case),):
    print(audio)
    todo = await todo_use_case.execute_post_todo(audio=audio, token=token)
    return todo
