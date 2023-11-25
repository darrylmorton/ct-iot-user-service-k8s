import asyncio
import logging
import unittest

import pytest
from sqlalchemy import delete

from tests.helper.db import get_db
from tests.helper.db import AsyncSessionLocal
from src.models import User

from tests.helper.routes import http_client, TEST_URL

LOGGER = logging.getLogger("user-service")

# db_conn = AsyncSessionLocal()

# events = []


class Test(unittest.IsolatedAsyncioTestCase):
    # @classmethod
    # @pytest.mark.asyncio
    async def asyncSetUp(self):
        logging.info(f"setUpClass")
        # cls.db_conn = AsyncSessionLocal()
        # # events.append("asyncSetUp")
        #
        # # db_conn.execute(delete(User))
        # # db_conn = get_db()
        # # await self.db_conn.execute(delete(User))
        # # self._async_connection = AsyncSessionLocal()
        # await cls.db_conn.execute(delete(User))
        # # await self._async_connection.close()

    # @classmethod
    # @pytest.mark.asyncio
    async def asyncTearDown(self):
        logging.info(f"tearDownClass")

        # events.append("asyncTearDown")
        # await self.db_conn.close()

    # @pytest.mark.asyncio
    async def test_health(self) -> None:
        # response = await http_client(TEST_URL, "/healthz")
        #
        # assert response.status_code == 200
        # assert response.json() == {"message": "ok"}
        logging.info(f"test_health")

    # @pytest.mark.asyncio
    async def test_post_user(self) -> None:
        logging.info(f"test_post_user")

        # # await self.asyncSetUp(self)
        # user = User(username="hi", password_hash="ho", salt="he", enabled=True)
        # # db = AsyncSessionLocal()
        #
        # await self.db_conn.execute(delete(User))
        # self.db_conn.add_all([user])
        # await self.db_conn.commit()

        # db_conn.add_all([user])
        # await db_conn.commit()

        # self._async_connection.add_all([user])
        # await self._async_connection.commit()
        # await self._async_connection.close()

        # await db.close()

        # results = await get_users(db)
        # # await db.close()
        # logging.info(f"*** TEST results {results[0]}")
        # assert results.length == 1


# asyncio.run()
