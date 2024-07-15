from abc import abstractmethod, ABCMeta
from typing import Optional

from volcano.domain.entity.user import VolcanoUser
from volcano.domain.entity.user_info import UserInfo


class UserRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_user_info(self, volcano_user: VolcanoUser) -> Optional[UserInfo]:
        ...

    @abstractmethod
    def delete_user(self, user_id: str):
        ...
