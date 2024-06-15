# NOTE You can write execute method in TodoUseCase class, the methods must be from infrastructure/repository/todo/todo_repository_impl file
# NOTE Execute command is for executing repository file's methods
# NOTE You must name each method like executeCreateTodo, executeReadTodo

from abc import abstractmethod, ABCMeta
# from .todo_model import TodoPostModel
from typing import Optional
from volcano.domain.entity.todo import Todo
from fastapi import HTTPException, UploadFile



from ...infrastructure.repository.todo.todo_repository_impl import TodoRepository
from ...infrastructure.repository.auth.auth_repository_impl import AuthRepository


from ...domain.repository.todo.todo_repository import TodoRepository

class TodoUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def execute_post_todo(self, audio: UploadFile, token: str) -> Optional[Todo]:
        ...

class TodoUseCaseImpl(TodoUseCase):

    def __init__(self, todo_repository: TodoRepository, auth_repository: AuthRepository):
        self.todo_repository: TodoRepository = todo_repository
        self.auth_repository: AuthRepository = auth_repository

    async def execute_post_todo(self, audio: UploadFile, token: str) -> Optional[Todo]:
        try:
            user_id = self.auth_repository.get_current_user(token).user_id
        except:
            raise HTTPException(status_code=404, detail="User not found")

        if user_id == None:
            raise HTTPException(status_code=404, detail="User not found")

        bytes_audio = await audio.read()

        if bytes_audio == None:
            raise HTTPException(status_code=302, detail="Can't load the audio")

        todo = self.todo_repository.post_todo(user_id=user_id, bytes_audio=bytes_audio)

        if todo == None:
            raise HTTPException(status_code=302, detail="Can't add this todo")


        return todo
