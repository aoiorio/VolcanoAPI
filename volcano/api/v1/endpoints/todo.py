from fastapi import APIRouter, Depends, UploadFile, File
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ....use_case.todo import TodoUseCase, TodoUseCaseImpl
from ....infrastructure.repository.todo import (
    TodoRepository,
    TodoRepositoryImpl,
)
from ....infrastructure.repository.auth import (
    AuthRepository,
    AuthRepositoryImpl,
)
from ....use_case.model.todo import TodoPostModel


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
async def post_todo(
    token: str,
    data: TodoPostModel = Depends(),
    todo_use_case: TodoUseCase = Depends(todo_use_case),
    audio: UploadFile = File(...),
):
    # print(audio)
    todo = await todo_use_case.execute_post_todo(token=token, data=data, audio=audio)
    return todo


@router.get("/text-to-todo/")
async def text_to_todo(
    voice_text: str,
    todo_use_case: TodoUseCase = Depends(todo_use_case),
):
    todo = todo_use_case.execute_text_to_todo(voice_text)
    return todo
    # return await todo_use_case.execute_text_to_todo(voice_text)
