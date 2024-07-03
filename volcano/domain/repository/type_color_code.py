from abc import abstractmethod, ABCMeta
from typing import Optional
from ..entity.type_color_code import TypeColorCode


class TypeColorCodeRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def add_type_color_object(self, type: str) -> Optional[TypeColorCode]:
        ...

    @abstractmethod
    def is_type_exist(self, type: str) -> Optional[bool]:
        ...

    @abstractmethod
    def read_type_color_codes(self) -> Optional[list[TypeColorCode]]:
        ...
