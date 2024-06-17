from abc import abstractmethod, ABCMeta
# from .. import SignUpUserModel, SignInUserModel
from typing import Optional
from volcano.domain.entity.user import VolcanoUser
from fastapi import HTTPException
from ..domain.repository.user import UserRepository


class UserUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def find_user_info(self, token: str) -> Optional[VolcanoUser]:
        ...


class UserUseCaseImpl(UserUseCase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        # self.auth_repository: AuthRepository = AuthRepositoryImpl

    def find_user_info(self, token: str) -> Optional[VolcanoUser]:
        try:
            # token = request.cookies.get("access_token")
            if token is None:
                raise HTTPException(status_code=401, detail="You haven't signed in")
            volcano_user = self.user_repository.get_user_info(token)

            if volcano_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return volcano_user
        except:
            raise
