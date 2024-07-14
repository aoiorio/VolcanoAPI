# NOTE You can write execute method in TodoUseCase class, the methods must be from infrastructure/repository/todo/todo_repository_impl file
# NOTE Execute command is for executing repository file's methods
# NOTE You must name each method like executeCreateTodo, executeReadTodo

from abc import abstractmethod, ABCMeta

# from .todo_model import TodoPostModel
from typing import Optional
from volcano.domain.entity.goal_percentage import GoalPercentage
from volcano.domain.entity.read_todo import ReadTodo
from volcano.domain.entity.todo import Todo
from fastapi import HTTPException, UploadFile, File
from volcano.domain.repository.type_color_code import TypeColorCodeRepository

from ..infrastructure.repository.todo import TodoRepository
from ..infrastructure.repository.auth import AuthRepository
from .model.todo import TodoPostModel
from jose import JWTError


class TodoUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def execute_post_todo(
        self, token: str, data: TodoPostModel, audio: UploadFile = File(...),
    ) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_post_todo_from_text(self, token: str, data: TodoPostModel) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_text_to_todo(self, voice_text: str) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_read_todo(self, token: str) -> Optional[list[ReadTodo]]:
        ...

    @abstractmethod
    def execute_update_todo(self, todo_id: str, new_todo: Todo) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_delete_todo(self, todo_id: str) -> Optional[Todo]:
        ...

    @abstractmethod
    def execute_get_goal_percentage(self, token: str) -> Optional[GoalPercentage]:
        ...


class TodoUseCaseImpl(TodoUseCase):

    def __init__(
        self, todo_repository: TodoRepository, auth_repository: AuthRepository, type_color_code_repository: TypeColorCodeRepository
    ):
        self.todo_repository: TodoRepository = todo_repository
        self.auth_repository: AuthRepository = auth_repository
        self.type_color_code_repository: TypeColorCodeRepository = type_color_code_repository

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

        is_type_exist = self.type_color_code_repository.is_type_exist(type=data.type)

        if is_type_exist:
            self.type_color_code_repository.add_type_color_object(type=data.type)

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

    def execute_post_todo_from_text(self, token: str, data: TodoPostModel) -> Optional[Todo]:
        try:
            user_id = self.auth_repository.get_current_user(token).user_id
        except:
            raise HTTPException(status_code=404, detail="User not found")

        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        is_type_exist = self.type_color_code_repository.is_type_exist(type=data.type)
        print(is_type_exist)

        if is_type_exist:
            self.type_color_code_repository.add_type_color_object(type=data.type)

        todo = self.todo_repository.post_todo_from_text(
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

    def execute_read_todo(self, token: str) -> Optional[list[ReadTodo]]:
        try:
            user_id = self.auth_repository.get_current_user(token=token).user_id
            if user_id is None:
                raise HTTPException(status_code=404, detail="User Not Found, Please SignIn")
            user_todo = self.todo_repository.read_todo(user_id=user_id)

            return user_todo
        except JWTError:
            raise HTTPException(status_code=404, detail="User not found")
        except:
            raise HTTPException(status_code=404, detail="Something went wrong")

    def execute_update_todo(self, todo_id: str, new_todo: Todo) -> Optional[Todo]:
        try:
            self.todo_repository.update_todo(todo_id=todo_id, new_todo=new_todo)
        except:
            raise HTTPException(status_code=404, detail="Something went wrong")

        raise HTTPException(status_code=204, detail="Todo Updated")

    def execute_delete_todo(self, todo_id: str) -> Optional[Todo]:
        try:
            self.todo_repository.delete_todo(todo_id=todo_id)
        except:
            raise HTTPException(status_code=404, detail="Something went wrong")

        raise HTTPException(status_code=204, detail="Todo Deleted")

    def execute_get_goal_percentage(self, token: str) -> Optional[GoalPercentage]:
        if token is None:
            raise HTTPException(status_code=404, detail="Token is none")
        # user_todo: list[Todo] = self.execute_read_todo(token=token)
        try:
            user_id = self.auth_repository.get_current_user(token=token).user_id
        except:
            raise HTTPException(status_code=404, detail="User not found")

        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.todo_repository.get_goal_percentage(user_id=user_id)
