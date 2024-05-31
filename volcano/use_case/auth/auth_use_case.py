# from ...infrastructure.repository.auth.auth_repository_impl import AuthRepositoryImpl
from abc import ABC, abstractmethod, ABCMeta
from .auth_model import SignUpUserModel, SignInUserModel
from typing import Optional
from volcano.domain.entity.user import VolcanoUser
# from ...infrastructure.postgresql.dto.volcano_user_dto import VolcanoUserDTO
from fastapi import HTTPException, Request
from fastapi.responses import Response
from jose import JWTError

from ...domain.repository.auth.auth_repository import AuthRepository

class AuthUseCase(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def sign_up_user(self, data: SignUpUserModel) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def sign_in_user(self, data: SignInUserModel, response: Response, request: Request) -> Optional[str]:
        ...

    @abstractmethod
    def sign_out_user(self, response: Response, request: Request) -> Optional[VolcanoUser]:
        ...

    @abstractmethod
    def get_current_user(self, request: Request) -> Optional[VolcanoUser]:
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

        # NOTE ** means allocating values to VolcanoUser
        # NOTE hashed_password is not hashed yet
        volcano_user = VolcanoUser(email=data.email, hashed_password=data.password)

        self.auth_repository.sign_up(volcano_user)

        return volcano_user

    # I think that this can return volcano_user object
    def sign_in_user(self, data: SignInUserModel, response: Response, request: Request) -> Optional[str]:
        # NOTE maybe you can replace existing_user to get_current_user.
        existing_user = self.auth_repository.find_by_email(data.email)

        # NOTE block not existing user
        if existing_user == None:
            print("existing_user")
            raise HTTPException(status_code=302, detail="User not found")

        # NOTE check the password is correct or not
        is_correct_password = self.auth_repository.verify_user_password(data.password, existing_user.hashed_password)

        if not is_correct_password:
            raise HTTPException(status_code=302, detail="Password is wrong")

        # NOTE check wether the user has already signed in or not
        token = request.cookies.get("access_token")

        if token != None:
            self.auth_repository.sign_out(response)
            # raise HTTPException(status_code=302, detail="You have already signed in")

        # NOTE user sign in feature
        access_token = self.auth_repository.sign_in(existing_user.user_id, response)

        if access_token == None:
            raise HTTPException(status_code=404, detail="Something went wrong. Please try again")

        return access_token

    def sign_out_user(self, response: Response, request: Request):

        token = request.cookies.get("access_token")

        if token == None:
            raise HTTPException(status_code=302, detail="User not found")

        self.auth_repository.sign_out(response)

    # FIXME - I think get_current_user in auth_user_case is redundant
    def get_current_user(self, request: Request) -> Optional[VolcanoUser]:
        try:
            token = request.cookies.get("access_token")
            if token == None:
                raise HTTPException(status_code=302, detail="User not found")

            volcano_user = self.auth_repository.get_current_user(token)

            if volcano_user == None:
                raise HTTPException(status_code=302, detail="User not found")

            return volcano_user
        except JWTError:
            raise HTTPException(status_code=404, detail="Not Found")
