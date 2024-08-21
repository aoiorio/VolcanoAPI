from fastapi import APIRouter, Depends
from volcano.domain.repository.type_color_code import TypeColorCodeRepository
from volcano.infrastructure.repository.type_color_code import (
    TypeColorCodeRepositoryImpl,
)
from ....infrastructure.postgresql.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....use_case.type_color_code import TypeColorCodeUseCase, TypeColorCodeUseCaseImpl


router = APIRouter(
    prefix="/type-color-code",
    tags=["type-color-code"],
)


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def type_color_code_use_case(db: Session = Depends(get_db)) -> TypeColorCodeUseCase:
    # NOTE ここでrepositoryをrepositoryImplにしている
    type_color_code_repository: TypeColorCodeRepository = TypeColorCodeRepositoryImpl(
        db=db
    )
    return TypeColorCodeUseCaseImpl(type_color_code_repository)


@router.get("/")
async def read_type_color_code(
    type_color_code_use_case: TypeColorCodeUseCase = Depends(type_color_code_use_case),
):
    type_color_code_list = type_color_code_use_case.execute_read_type_color_code()
    return type_color_code_list
