import pytest
from sqlalchemy import delete
from sqlalchemy.sql.operators import add

# from crud import add_user
# from .helper.user_helper import create_user_payload
from src.models import UserModel
from src.database import async_engine


# TODO replace with session and use a db helper delete?
@pytest.fixture()
async def db_cleanup():
    engine = async_engine

    async with engine.begin() as conn:
        await conn.execute(delete(UserModel))

    await engine.dispose()


# @pytest.fixture()
# async def db_user_enabled():
#     user = create_user(_enabled=True)
#     user = await add_user(_username=user.username, _password=user.password)
#     engine = async_engine
#
#     async with engine.begin() as conn:
#         await conn.execute(add(user))
#
#     await engine.dispose()
