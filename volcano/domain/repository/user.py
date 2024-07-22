from abc import abstractmethod, ABCMeta
from typing import Optional

from volcano.domain.entity.user import VolcanoUser
from volcano.domain.entity.user_info import UserInfo
from volcano.use_case.model.user import UpdateUserModel


class UserRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_user_info(self, volcano_user: VolcanoUser) -> Optional[UserInfo]:
        ...

    @abstractmethod
    def delete_user(self, user_id: str):
        ...

    @abstractmethod
    def update_user(self, user_id: str, updated_user: UpdateUserModel):
        ...
