from abc import abstractmethod, ABCMeta
from typing import Optional
from fastapi import UploadFile
from pydantic.dataclasses import dataclass
from ...entity.todo import Todo


class TodoRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def post_todo(self, user_id: str, bytes_audio: bytes) -> Optional[Todo]:
        ...