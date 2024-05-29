from fastapi import APIRouter, Depends
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

from ....infrastructure.postgresql.dto.volcano_user_dto import VolcanoUserDTO
from ....infrastructure.repository.auth.auth_repository_impl import AuthRepository, AuthRepositoryImpl

from ....use_case.auth.auth_model import SignInUserModel, SignUpUserModel
from ....use_case.auth.auth_use_case import AuthUseCaseImpl, AuthUseCase

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_db():
    db: Session = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def auth_use_case(db: Session = Depends(get_db)) -> AuthUseCase:
    """Get a book command use case."""
    # NOTE ここでrepositoryをrepositoryImplにしている
    auth_repository: AuthRepository = AuthRepositoryImpl(db=db)
    # repository: AuthRepositoryImpl
    return AuthUseCaseImpl(auth_repository)

@router.post("/create_user")
async def create_user(data: SignUpUserModel, auth_use_case: AuthUseCase = Depends(auth_use_case)):
    print("hello create user method")
    print(data)
    volcano_user = auth_use_case.sign_up_user(data)
    return volcano_user

