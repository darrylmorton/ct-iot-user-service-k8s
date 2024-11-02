import uuid

from sqlalchemy import select

from database import models
from database.user_crud_stmt_interface import UserCrudStmtInterface


class UserCrudStmt(UserCrudStmtInterface):
    def add_user_model(self, username: str, password_hash: str):
        return models.UserModel(username=username, password_hash=password_hash)

    def find_user_by_id_stmt(self, _id: str):
        return select(models.UserModel).where(_id == models.UserModel.id)

    def find_user_by_username_stmt(self, username: str):
        return select(models.UserModel).where(username == models.UserModel.username)

    def update_confirmed(self, _id: uuid.UUID, _confirmed: bool):
        # stmt = (
        #     sa.update(UserProfileModel)
        #     .where(UserProfileModel.id == user_id)
        #     .values(**payload.dict())
        # )
        # result = await db.execute(stmt)

        result = select(models.UserModel).where(_id == models.UserModel.id)
        # .update(_confirmed=_confirmed)
        # )

        return result.update(_confirmed=_confirmed)
