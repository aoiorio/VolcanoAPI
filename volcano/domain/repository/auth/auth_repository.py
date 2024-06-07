from abc import abstractmethod, ABCMeta
from typing import Optional

from pydantic.dataclasses import dataclass
from ...entity.user import VolcanoUser
from fastapi.responses import Response
from fastapi import Request

class AuthRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def verify_user_password(self, plain_password: str, hashed_password: str) -> bool:
        ...

    @abstractmethod
    def sign_up(self, volcano_user: VolcanoUser, response: Response) -> Optional[str]:
        ...

    @abstractmethod
    def sign_in(self, user_id: str, response: Response) -> Optional[str]:
        ...

    @abstractmethod
    def sign_out(self, response: Response) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def get_current_user(self, token: str) -> Optional[VolcanoUser]:
        ...