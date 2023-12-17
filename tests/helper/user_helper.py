import json

import bcrypt

from tests.database import async_session
from src.schemas import User
from src.models import UserModel
# from ..database import async_session
# from src.database import get_db


def create_user_payload(_username: str, _password: str):
    return json.dumps({"username": _username, "password": _password})
    # return {"username": _username, "password": _password}


# async def delete_users():
#     async with async_session() as session:
#         async with session.begin():
#             session.delete(UserModel)
#             await session.commit()


async def add_test_user(_username: str, _password: str, _enabled=False):
    # user = create_user(_username, _password, _enabled)
    password = _password.encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")
    user = UserModel(
        username=_username, password_hash=password_hash, enabled=_enabled
    )

    async with async_session() as session:
        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return User(id=user.id, username=user.username, enabled=_enabled)
