from sqlalchemy import select

from database import models
from database.user_crud_stmt_interface import UserCrudStmtInterface


class UserCrudStmt(UserCrudStmtInterface):
    def add_user_model(self, username: str, password_hash: str):
        return models.UserModel(username=username, password_hash=password_hash)

    def find_user_by_id_stmt(self, _id: str):
        return select(models.UserModel).where(_id == models.UserModel.id)

    # def find_user_by_id_and_enabled_stmt(self, _id: str):
    #     return select(models.UserModel).where(
    #         _id == models.UserModel.id,
    #         models.UserModel.enabled,
    #     )

    def find_user_by_username_stmt(self, username: str):
        return select(models.UserModel).where(username == models.UserModel.username)

    def find_user_by_id_and_confirmed_and_enabled_stmt(self, _id: str):
        return select(models.UserModel).where(
            _id == models.UserModel.id,
            models.UserModel.confirmed,
            models.UserModel.enabled,
        )
