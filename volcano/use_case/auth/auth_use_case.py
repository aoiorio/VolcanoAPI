from ...infrastructure.repository.auth.auth_repository_impl import AuthRepositoryImpl
from abc import ABC, abstractmethod, ABCMeta
from .auth_model import SignUpUserModel, SignInUserModel
from typing import Optional
from volcano.domain.entity.user import VolcanoUser
from ...infrastructure.postgresql.dto.volcano_user_dto import VolcanoUserDTO
from fastapi import HTTPException
from ...domain.repository.auth.auth_repository import AuthRepository

class AuthUseCase(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def __init__(self, auth_repository: AuthRepository):
        ...

    @abstractmethod
    def sign_up_user(self, data: SignUpUserModel) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def sign_in_user(self, data: SignInUserModel) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def sign_out_user(self) -> Optional[VolcanoUser]:
        ...

class AuthUseCaseImpl(AuthUseCase):

    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository: AuthRepository = auth_repository

    def sign_up_user(self, data: SignUpUserModel) -> Optional[VolcanoUser]:
        if data.password != data.confirm_password:
            raise HTTPException(status_code=404, detail="Confirm password is different")

        existing_user = self.auth_repository.find_by_email(email=data.email)

        if existing_user != None:
            raise HTTPException(status_code=302, detail="This user exists")

        # hashed_password = self.auth_repository.

        # NOTE ** means allocating values to VolcanoUser
        # NOTE hashed_password is not hashed yet
        print(f"data is here: {data}")
        volcano_user = VolcanoUser(email=data.email, hashed_password=data.password)
        # print(volcano_user)
        print(f"volcano_user is here: {volcano_user}")

        self.auth_repository.sign_up(volcano_user)

        return volcano_user

    def sign_in_user(self, data: SignInUserModel):
        return super().sign_in_user(data)

    def sign_out_user(self):
        return super().sign_out_user()
