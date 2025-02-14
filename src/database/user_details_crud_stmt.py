import uuid

from sqlalchemy import select

from database import models
from database.user_details_crud_stmt_interface import UserDetailsCrudStmtInterface


class UserDetailsCrudStmt(UserDetailsCrudStmtInterface):
    def add_user_details_model(self, user_id: uuid, first_name: str, last_name: str):
        return models.UserDetailsModel(
            user_id=user_id, first_name=first_name, last_name=last_name
        )

    def find_user_details_by_user_id_stmt(self, user_id: int, offset=0):
        return (
            select(
                models.UserDetailsModel.id,
                models.UserDetailsModel.first_name,
                models.UserDetailsModel.last_name,
            )
            .where(models.UserDetailsModel.user_id == user_id)
            .limit(25)
            .offset(offset)
        )
