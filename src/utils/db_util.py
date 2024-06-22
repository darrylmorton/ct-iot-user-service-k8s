from sqlalchemy import select

from models import UserModel


def find_users_stmt(offset=0):
    return select(UserModel).limit(25).offset(offset)


def find_user_by_username_stmt(username: str):
    return select(UserModel).where(username == UserModel.username)
