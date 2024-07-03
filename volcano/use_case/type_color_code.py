
from abc import abstractmethod, ABCMeta

from typing import Optional
from fastapi import HTTPException

from ..infrastructure.repository.type_color_code import TypeColorCodeRepository
from ..domain.entity.type_color_code import TypeColorCode


class TypeColorCodeUseCase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def execute_read_type_color_code(self) -> Optional[list[TypeColorCode]]:
        ...


class TypeColorCodeUseCaseImpl(TypeColorCodeUseCase):
    def __init__(self, type_color_code_repository: TypeColorCodeRepository):
        self.type_color_code_repository: TypeColorCodeRepository = type_color_code_repository

    def execute_read_type_color_code(self) -> Optional[list[TypeColorCode]]:
        try:
            type_color_code_list = self.type_color_code_repository.read_type_color_codes()
            return type_color_code_list
        except:
            raise HTTPException(status_code=404, detail="Something went wrong")
