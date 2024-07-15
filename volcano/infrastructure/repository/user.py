from volcano.domain.entity.user_info import UserInfo
from volcano.infrastructure.postgresql.dto.todo import TodoDTO
from ...domain.repository.user import UserRepository
from ...domain.entity.user import VolcanoUser

from typing import Optional
from sqlalchemy.orm import Session


class UserRepositoryImpl(UserRepository):

    def __init__(self, db: Session):
        self.db: Session = db

    def get_user_info(self, volcano_user: VolcanoUser) -> Optional[UserInfo]:
        user_id = volcano_user.user_id

        try:
            done_todo_dto = (
                self.db.query(TodoDTO)
                .filter_by(user_id=user_id, is_completed=True)
                .all()
            )

            not_yet_todo_dto = (
                self.db.query(TodoDTO)
                .filter_by(user_id=user_id, is_completed=False)
                .all()
            )

            return UserInfo(
                user_id=user_id,
                username=volcano_user.username,
                email=volcano_user.email,
                icon=volcano_user.icon,
                done_todo_num=len(done_todo_dto),
                not_yet_todo_num=len(not_yet_todo_dto),
            )
        except:
            raise
