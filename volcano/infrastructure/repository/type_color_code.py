from typing import Optional
import random
from sqlalchemy.orm.session import Session


# NOTE project imports
from volcano.domain.repository.type_color_code import TypeColorCodeRepository
from ...domain.entity.type_color_code import TypeColorCode
from ..postgresql.dto.type_color_code import TypeColorCodeDTO


def gen_random_color_code():
    # Generating a random number in between 0 and 2^24
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color


class TypeColorCodeRepositoryImpl(TypeColorCodeRepository):
    def __init__(self, db: Session):
        self.db: Session = db

    def add_type_color_object(self, type: str) -> Optional[TypeColorCode]:
        # NOTE generate hex color codes
        start_color_code = gen_random_color_code()
        end_color_code = gen_random_color_code()

        type_color_object = TypeColorCode(type=type, start_color_code=start_color_code, end_color_code=end_color_code)
        type_color_code_dto = TypeColorCodeDTO.from_entity(type_color_object=type_color_object)

        try:
            self.db.add(type_color_code_dto)
            self.db.commit()
            return type_color_code_dto.to_entity()
        except:
            raise

    def is_type_exist(self, type: str) -> Optional[bool]:
        try:
            type_color_code_dto = self.db.query(TypeColorCodeDTO).filter_by(type=type).first()
            # NOTE return the bool whether type exists or not
            return type_color_code_dto is None
        except:
            raise

    def read_type_color_codes(self) -> Optional[list[TypeColorCode]]:
        try:
            type_color_code_dto = self.db.query(TypeColorCodeDTO).all()
            return type_color_code_dto
        except:
            raise
