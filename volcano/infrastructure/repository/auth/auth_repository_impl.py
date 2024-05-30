from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from fastapi.responses import Response

from volcano.domain.entity.user import VolcanoUser
from ...postgresql.dto.volcano_user_dto import VolcanoUserDTO
from ....domain.repository.auth.auth_repository import AuthRepository
from ....core.config import SECRET_KEY, ALGORITHM


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create hash password
def create_password_hash(user_password: str):
    return bcrypt_context.hash(user_password)


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
            volcano_user_dto = self.db.query(VolcanoUserDTO).filter_by(user_id=user_id).first()
        except NoResultFound:
            return None
        except:
            raise
        return volcano_user_dto # this will cause an error volcano_user_dto.to_entity()

    def find_by_email(self, email: str) -> Optional[VolcanoUser]:
        # hashed_password = create_password_hash(user_password)
        try:
            volcano_user_dto = self.db.query(VolcanoUserDTO).filter_by(email=email).first()
        except:
            raise
        return volcano_user_dto

    # verify passwords that users inputted and hashed password
    def verify_user_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt_context.verify(plain_password, hashed_password)

    def sign_up(self, volcano_user: VolcanoUser) -> Optional[VolcanoUser]:
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
        except:
            raise

    def sign_in(self, user_id: str) -> Optional[VolcanoUser]:
        response = Response
        try:
            access_token = create_access_token(data={'sub': user_id}, expires_delta=300)
            response.set_cookie(key="access_token", value=access_token, httponly=True)
        except:
            raise

    def sign_out(self) -> Optional[VolcanoUser]:
        response = Response

        try:
            response.delete_cookie(key="access_token")
        except:
            raise