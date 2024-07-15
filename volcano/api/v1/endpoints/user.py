from fastapi import APIRouter, Depends
from volcano.domain.repository.auth import AuthRepository
from volcano.infrastructure.repository.auth import AuthRepositoryImpl

# from fastapi.responses import Response
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....use_case.user import UserUseCase, UserUseCaseImpl
from ....infrastructure.repository.user import UserRepository, UserRepositoryImpl


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_db():
    db: Session = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def user_use_case(db: Session = Depends(get_db)) -> UserUseCase:
    # NOTE ここでrepositoryをrepositoryImplにしている
    user_repository: UserRepository = UserRepositoryImpl(db=db)
    auth_repository: AuthRepository = AuthRepositoryImpl(db=db)
    return UserUseCaseImpl(user_repository, auth_repository)


@router.get("/")
async def get_user_info(
    token: str,
    user_use_case: UserUseCase = Depends(user_use_case),
):
    user_info = user_use_case.execute_get_user_info(token)
    return user_info


@router.delete("/")
async def delete_user(
    token: str,
    user_use_case: UserUseCase = Depends(user_use_case),
):
    user_use_case.execute_delete_user(token=token)
