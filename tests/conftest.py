import asyncio

import bcrypt
import pytest
from sqlalchemy import delete
from sqlalchemy.sql.operators import add

# from crud import add_user
# from .helper.user_helper import create_user_payload
from src.models import UserModel
from tests.database import async_session
# from src.database import get_db


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# TODO replace with session and use a db helper delete?
@pytest.fixture()
async def db_cleanup():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(UserModel))
            await session.commit()
            await session.close()

    # engine = async_engine
    #
    # async with engine.begin() as conn:
    #     await conn.execute(delete(UserModel))
    #
    # await engine.dispose()
# async def delete_users():


# @pytest.fixture()
# async def add_test_user(_username: str, _password: str, _enabled=False):
#     # user = create_user(_username, _password, _enabled)
#     password = _password.encode("utf-8")
#
#     salt = bcrypt.gensalt()
#     password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")
#     # user = UserModel(username=_username, password_hash=password_hash, enabled=_enabled)








    # engine = async_engine
    #
    # async with engine.begin() as conn:
    #     await conn.execute(add(UserModel(username=_username, password_hash=password_hash, enabled=_enabled)))
    #
    # await engine.dispose()

    # async with async_session() as session:
    #     user = UserModel(
    #         username=_username, password_hash=password_hash, enabled=_enabled
    #     )
    #
    #     async with session.begin():
    #         session.add(user)
    #         await session.commit()
    #
    #     await session.refresh(user)
    #     await session.close()
    #
    #     return User(id=user.id, username=user.username, enabled=_enabled)

# async def db_user_enabled():
#     user = create_user(_enabled=True)
#     user = await add_user(_username=user.username, _password=user.password)
#     engine = async_engine
#
#     async with engine.begin() as conn:
#         await conn.execute(add(user))
#
#     await engine.dispose()
