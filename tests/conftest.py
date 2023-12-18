import asyncio
import bcrypt
import pytest
from sqlalchemy import delete

from src.schemas import User
from src.models import UserModel
from tests.database import async_session


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def db_cleanup():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(UserModel))
            await session.commit()
            await session.close()


@pytest.fixture(scope="function")
async def add_test_user(request):
    user_request = request.param[0]

    password = user_request["password"].encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")
    user = UserModel(username=user_request["username"], password_hash=password_hash, enabled=user_request["enabled"])

    async with async_session() as session:
        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return User(id=user.id, username=user.username, enabled=user_request["enabled"])
