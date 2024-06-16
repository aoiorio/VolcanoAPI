from fastapi import APIRouter, Depends
# from fastapi.responses import Response
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....use_case.user.user_use_case import UserUseCase, UserUseCaseImpl
from ....infrastructure.repository.user.user_repository_impl import UserRepository, UserRepositoryImpl


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
    """Get a book command use case."""
    # NOTE ここでrepositoryをrepositoryImplにしている
    user_repository: UserRepository = UserRepositoryImpl(db=db)
    return UserUseCaseImpl(user_repository)


@router.get("/")
async def get_user_info(token: str, user_use_case: UserUseCase = Depends(user_use_case)):
    volcano_user = user_use_case.find_user_info(token)
    return volcano_user
