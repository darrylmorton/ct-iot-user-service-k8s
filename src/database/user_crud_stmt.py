from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.sql.dml import ReturningUpdate

from database import models
from database.models import UserModel
from database.user_crud_stmt_interface import UserCrudStmtInterface


class UserCrudStmt(UserCrudStmtInterface):
    def add_user_model(self, username: str, password_hash: str):
        return models.UserModel(username=username, password_hash=password_hash)

    def find_user_by_id_stmt(self, _id: str):
        return select(
            models.UserModel.id,
            models.UserModel.username,
            models.UserModel.confirmed,
            models.UserModel.is_admin,
            models.UserModel.enabled,
        ).where(models.UserModel.id == _id)

    def find_user_by_username_stmt(self, username: str):
        return select(
            models.UserModel.id,
            models.UserModel.username,
            models.UserModel.password_hash,
            models.UserModel.enabled,
            models.UserModel.confirmed,
            models.UserModel.is_admin,
        ).where(models.UserModel.username == username)

    def find_user_by_username_and_confirmed_stmt(self, username: str):
        return select(models.UserModel.id, models.UserModel.username).where(
            models.UserModel.username == username
        )

    def update_confirmed(
        self, _username: str, _confirmed: bool
    ) -> ReturningUpdate[tuple[UUID, str, bool]]:
        return (
            update(UserModel)
            .where(models.UserModel.username == _username)
            .values({"confirmed": _confirmed})
            .returning(UserModel.id, UserModel.username, UserModel.confirmed)
        )
