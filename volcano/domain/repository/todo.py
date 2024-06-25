from abc import abstractmethod, ABCMeta
from typing import Optional
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
