from typing import Optional

from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import Response

# from http.client import HTTPResponse
from volcano.domain.entity.user import VolcanoUser
from ..postgresql.dto.volcano_user import VolcanoUserDTO
from ...domain.repository.auth import AuthRepository
from ...core.config import SECRET_KEY, ALGORITHM
from passlib.hash import argon2


# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create hash password
def create_password_hash(user_password: str):
    print("create_password_hash!!")
    hashed_password = argon2.using(
        time_cost=1,
        memory_cost=2**16,
        parallelism=4,
        salt_size=128,
        digest_size=256,
    ).hash(user_password)

    return hashed_password


# create access token for signIn and signUp
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class AuthRepositoryImpl(AuthRepository):

    def __init__(self, db: Session):
        self.db: Session = db

    def find_by_id(self, user_id: str) -> Optional[VolcanoUser]:
        try:
            volcano_user_dto = (
                self.db.query(VolcanoUserDTO).filter_by(user_id=user_id).first()
            )
        except:
            raise
        # this will cause an error volcano_user_dto.to_entity()
        return volcano_user_dto

    def find_by_email(self, email: str) -> Optional[VolcanoUser]:
        # hashed_password = create_password_hash(user_password)
        try:
            volcano_user_dto = (
                self.db.query(VolcanoUserDTO).filter_by(email=email).first()
            )
        except:
            raise
        return volcano_user_dto

    # verify passwords that users inputted and hashed password
    def verify_user_password(self, plain_password: str, hashed_password: str) -> bool:
        return argon2.verify(plain_password, hashed_password)

    def sign_up(self, volcano_user: VolcanoUser, response: Response) -> Optional[str]:
        print(f"volcano_user from repository impl file is here {volcano_user}")
        # NOTE Get volcano user and define as volcano user dto for adding to database
        volcano_user_dto = VolcanoUserDTO.from_entity(volcano_user)

        # NOTE Get user password that was inputted by user
        user_password = volcano_user_dto.hashed_password

        # NOTE Create hashed_password from user_password
        volcano_user_dto.hashed_password = create_password_hash(user_password)
        try:
            # ! you don't have to do error handling here because you can do it on usecase files
            self.db.add(volcano_user_dto)
            self.db.commit()

            userEmail = self.find_by_email(volcano_user.email)
            access_token = self.sign_in(userEmail.user_id, response)
            print(access_token)
            return access_token
        except:
            raise

    def sign_in(self, user_id: str, response: Response) -> Optional[str]:
        # NOTE it's a different function from creating cookie , so you can do it in another function called sign_in_for_token() or you can rename this function to it.
        # NOTE Then it will return a string access token (JWT)
        try:
            access_token = create_access_token(
                data={
                    "sub": str(user_id),
                },
                expires_delta=300,
            )
            print(f"Here is access_token {access_token}")
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            return access_token
        except:
            raise

    def get_current_user(self, token: str) -> Optional[VolcanoUser]:
        # NOTE get request in an usecase file.
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            print(user_id)
            volcano_user_dto = (
                self.db.query(VolcanoUserDTO).filter_by(user_id=user_id).first()
            )

            return volcano_user_dto
        except JWTError:
            raise
        except:
            raise
