from abc import abstractmethod, ABCMeta
from typing import Optional

from volcano.domain.entity.goal_info import GoalInfo
from volcano.domain.entity.read_todo import ReadTodo
from ..entity.todo import Todo
from datetime import datetime
import uuid


class TodoRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def post_todo(self, user_id: uuid.UUID, bytes_audio: bytes, title: str, description: str, type: str, period: datetime, priority: int) -> Optional[Todo]:
        ...

    @abstractmethod
    def post_todo_from_text(self, user_id: uuid.UUID, title: str, description: str, type: str, period: datetime, priority: int) -> Optional[Todo]:
        ...

    @abstractmethod
    def text_to_todo(self, voice_text: str) -> Optional[Todo]:
        ...

    @abstractmethod
    def read_todo(self, user_id: uuid.UUID) -> Optional[list[ReadTodo]]:
        ...

    @abstractmethod
    def get_goal_info(self, user_id: uuid.UUID) -> Optional[GoalInfo]:
        ...

    @abstractmethod
    def update_todo(self, todo_id: str, new_todo: Todo) -> Optional[Todo]:
        ...

    @abstractmethod
    def delete_todo(self, todo_id: str) -> Optional[Todo]:
        ...
