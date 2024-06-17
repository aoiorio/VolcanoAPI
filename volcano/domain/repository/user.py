from abc import abstractmethod, ABCMeta
from typing import Optional
from ..entity.user import VolcanoUser
# from fastapi import Request


class UserRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_user_info(self, token: str) -> Optional[VolcanoUser]:
        ...
