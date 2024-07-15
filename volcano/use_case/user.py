from abc import abstractmethod, ABCMeta
# from .. import SignUpUserModel, SignInUserModel
from typing import Optional
from fastapi import HTTPException
from volcano.domain.entity.user_info import UserInfo
from volcano.domain.repository.auth import AuthRepository
# from volcano.infrastructure.repository.auth import AuthRepositoryImpl
from ..domain.repository.user import UserRepository


class UserUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def execute_get_user_info(self, token: str) -> Optional[UserInfo]:
        ...


class UserUseCaseImpl(UserUseCase):

    def __init__(self, user_repository: UserRepository, auth_repository: AuthRepository):
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    def execute_get_user_info(self, token: str) -> Optional[UserInfo]:
        try:
            volcano_user = self.auth_repository.get_current_user(token=token)
        except:
            raise HTTPException(status_code=404, detail="Something went wrong with getting user info")

        try:
            if volcano_user is None:
                raise HTTPException(status_code=404, detail="User not found")

            user_info = self.user_repository.get_user_info(volcano_user=volcano_user)

            return user_info
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Something went wrong")
