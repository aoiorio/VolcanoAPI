from fastapi import APIRouter, Depends, UploadFile, File
from volcano.domain.repository.type_color_code import TypeColorCodeRepository
from volcano.infrastructure.repository.type_color_code import TypeColorCodeRepositoryImpl
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....use_case.todo import TodoUseCase, TodoUseCaseImpl
from ....infrastructure.repository.todo import (
    TodoRepository,
    TodoRepositoryImpl,
)
from ....infrastructure.repository.auth import (
    AuthRepository,
    AuthRepositoryImpl,
)
from ....use_case.model.todo import TodoPostModel, TodoUpdateModel


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


def todo_use_case(db: Session = Depends(get_db)) -> TodoUseCase:
    # NOTE ここでrepositoryをrepositoryImplにしている
    todo_repository: TodoRepository = TodoRepositoryImpl(db=db)
    auth_repository: AuthRepository = AuthRepositoryImpl(db=db)
    type_color_code_repository: TypeColorCodeRepository = TypeColorCodeRepositoryImpl(db=db)
    return TodoUseCaseImpl(todo_repository, auth_repository, type_color_code_repository)


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


@router.post("/post-todo-from-text")
async def post_todo_from_text(token: str, data: TodoPostModel, todo_use_case: TodoUseCase = Depends(todo_use_case)):
    todo = todo_use_case.execute_post_todo_from_text(token=token, data=data)
    return todo


@router.delete("/")
async def delete_todo(todo_id: str, todo_use_case: TodoUseCase = Depends(todo_use_case)):
    todo_use_case.execute_delete_todo(todo_id=todo_id)


@router.put("/")
async def update_todo(
    todo_id: str,
    new_todo: TodoUpdateModel,
    todo_use_case: TodoUseCase = Depends(todo_use_case),
):
    todo_use_case.execute_update_todo(todo_id=todo_id, new_todo=new_todo)


@router.get("/text-to-todo/")
async def text_to_todo(
    voice_text: str,
    todo_use_case: TodoUseCase = Depends(todo_use_case),
):
    todo = todo_use_case.execute_text_to_todo(voice_text)
    return todo


@router.get("/user-todo/")
async def read_todo(
    token: str,
    todo_use_case: TodoUseCase = Depends(todo_use_case)
):
    user_todo = todo_use_case.execute_read_todo(token=token)
    return user_todo


@router.get("/user-goals/")
async def get_goal_percentage(
    token: str,
    todo_use_case: TodoUseCase = Depends(todo_use_case)
):
    goal_percentage = todo_use_case.execute_get_goal_percentage(token=token)
    return goal_percentage
