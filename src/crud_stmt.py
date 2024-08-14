import uuid

from sqlalchemy import select

import models
from abstract_crud_stmt import AbstractCrudStmt


class CrudStmt(AbstractCrudStmt):
    # Admin only, requires roles to be implemented
    def find_users_stmt(self, offset=0):
        return select(models.UserModel).limit(25).offset(offset)

    def find_user_by_username_stmt(self, username: str):
        return select(models.UserModel).where(username == models.UserModel.username)

    def find_user_by_id_stmt(self, _id: str):
        return select(models.UserModel).where(_id == models.UserModel.id)

    def find_user_by_id_and_enabled_stmt(self, _id: str):
        return select(models.UserModel).where(
            _id == models.UserModel.id,
            models.UserModel.enabled,
        )

    def add_user_model(self, username: str, password_hash: str):
        return models.UserModel(username=username, password_hash=password_hash)

    def find_user_details_stmt(self, offset=0):
        return select(models.UserDetailsModel).limit(25).offset(offset)

    def find_user_details_by_user_id_stmt(self, user_id: int, offset=0):
        return (
            select(models.UserDetailsModel)
            .where(user_id == models.UserDetailsModel.user_id)
            .limit(25)
            .offset(offset)
        )

    def add_user_details_model(self, user_id: uuid, first_name: str, last_name: str):
        return models.UserDetailsModel(
            user_id=user_id, first_name=first_name, last_name=last_name
        )
