# NOTE You can write execute method in TodoUseCase class, the methods must be from infrastructure/repository/todo/todo_repository_impl file
# NOTE Execute command is for executing repository file's methods
# NOTE You must name each method like executeCreateTodo, executeReadTodo

from abc import abstractmethod, ABCMeta

# from .todo_model import TodoPostModel
from typing import Optional
from volcano.domain.entity.todo import Todo
from fastapi import HTTPException, UploadFile, File

from ..infrastructure.repository.todo import TodoRepository
from ..infrastructure.repository.auth import AuthRepository
from .model.todo import TodoPostModel


class TodoUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def execute_post_todo(
        self, token: str, data: TodoPostModel, audio: UploadFile = File(...),
    ) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_text_to_todo(self, voice_text: str) -> Optional[Todo]:
        ...


class TodoUseCaseImpl(TodoUseCase):

    def __init__(
        self, todo_repository: TodoRepository, auth_repository: AuthRepository
    ):
        self.todo_repository: TodoRepository = todo_repository
        self.auth_repository: AuthRepository = auth_repository

    async def execute_post_todo(
        self, data: TodoPostModel, token: str, audio: UploadFile = File(...),
    ) -> Optional[Todo]:
        try:
            user_id = self.auth_repository.get_current_user(token).user_id
        except:
            raise HTTPException(status_code=404, detail="User not found")

        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        bytes_audio = await audio.read()

        if bytes_audio is None:
            raise HTTPException(status_code=302, detail="Can't load the audio")

        todo = self.todo_repository.post_todo(
            bytes_audio=bytes_audio,
            user_id=user_id,
            title=data.title,
            description=data.description,
            type=data.type,
            period=data.period,
            priority=data.priority,
        )

        if todo is None:
            raise HTTPException(status_code=302, detail="Can't add this todo")

        return todo

    def execute_text_to_todo(self, voice_text: str) -> Optional[Todo]:
        print(voice_text)
        # TODO execute repository text_to_todo method here
        text = self.todo_repository.text_to_todo(voice_text)
        return text
