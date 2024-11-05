from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.sql.dml import ReturningUpdate

from database import models
from database.models import UserModel
from database.user_crud_stmt_interface import UserCrudStmtInterface


class UserCrudStmt(UserCrudStmtInterface):
    def add_user_model(self, username: str, password_hash: str):
        return models.UserModel(username=username, password_hash=password_hash)

    def find_user_by_id_stmt(self, _id: str):
        return select(models.UserModel).where(_id == models.UserModel.id)

    def find_user_by_username_stmt(self, username: str):
        return select(models.UserModel).where(username == models.UserModel.username)

    def find_user_by_username_and_confirmed_stmt(self, username: str):
        return select(models.UserModel).where(username == models.UserModel.username)

    def update_confirmed(
        self, _username: str, _confirmed: bool
    ) -> ReturningUpdate[tuple[UUID, str, bool]]:
        return (
            update(UserModel)
            .where(UserModel.username == _username)
            .values({"confirmed": _confirmed})
            .returning(UserModel.id, UserModel.username, UserModel.confirmed)
        )
