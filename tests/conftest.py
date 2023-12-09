import pytest
from sqlalchemy import delete

from src.models import User
from src.database import async_engine


@pytest.fixture()
async def db_cleanup():
    engine = async_engine

    async with engine.begin() as conn:
        await conn.execute(delete(User))

    await engine.dispose()
