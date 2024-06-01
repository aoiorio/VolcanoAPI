from ....domain.repository.user.user_repository import UserRepository
from ....domain.repository.auth.auth_repository import AuthRepository
from ....infrastructure.repository.auth.auth_repository_impl import AuthRepositoryImpl

from ....domain.entity.user import VolcanoUser
from fastapi import Request
from typing import Optional
from sqlalchemy.orm import Session

class UserRepositoryImpl(UserRepository):

    def __init__(self, db: Session):
        self.auth_repository: AuthRepository = AuthRepositoryImpl(db=db)

    def get_user_info(self, token: str) -> Optional[VolcanoUser]:
        volcano_user = self.auth_repository.get_current_user(token)
        return volcano_user