from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status


from ....infrastructure.postgresql.dto.volcano_user_dto import VolcanoUserDTO
from ....infrastructure.repository.auth.auth_repository_impl import (
    AuthRepository,
    AuthRepositoryImpl,
)

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


@router.post("/sign_up_user")
async def sign_up_user(
    data: SignUpUserModel,
    response: Response,
    auth_use_case: AuthUseCase = Depends(auth_use_case),
):
    access_token = auth_use_case.sign_up_user(data, response)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign_in_user")
async def sign_in_user(
    request: Request,
    response: Response,
    data: SignInUserModel,
    auth_use_case: AuthUseCase = Depends(auth_use_case),
):
    # NOTE you can return user information if you want
    access_token = auth_use_case.sign_in_user(
        data=data, response=response, request=request
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/sign_out_user", status_code=status.HTTP_204_NO_CONTENT)
async def sign_out_user(
    request: Request,
    response: Response,
    auth_use_case: AuthUseCase = Depends(auth_use_case),
):
    auth_use_case.sign_out_user(response=response, request=request)
    return {"detail": "Successfully signed out"}
