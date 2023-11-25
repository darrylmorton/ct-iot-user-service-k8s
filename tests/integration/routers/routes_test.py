import json
import logging
from unittest import IsolatedAsyncioTestCase
from sqlalchemy import delete

from src.crud import get_users
from src.models import User
from tests.helper.routes import TEST_URL, http_post_client, http_client
from tests.helper.db import AsyncSessionLocal

LOGGER = logging.getLogger("user-service")


class UserTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.info(f"*** asyncSetUp")
        self.db_conn = AsyncSessionLocal()

        await self.db_conn.execute(delete(User))
        await self.db_conn.commit()
        # await self.db_conn.close()

    async def asyncTearDown(self):
        logging.info(f"*** asyncTearDown")

        # await self.db_conn.close()

    # async def test_post_user(self):
    #     payload = json.dumps(
    #         {"username": "foo", "password": "bar"}
    #     )
    #
    #     logging.info(f"*** test_post_users payload {payload}")
    #
    #     await http_post_client(TEST_URL, "/users", payload)
    #     response = await get_users(self.db_conn)
    #     actual_result = response.fetchall()
    #
    #     logging.info(f"*** test_post_users {actual_result}")
    #
    #     assert len(actual_result) == 1
    #     assert actual_result[0].username == "daz"

    async def test_get_by_user_username(self):
        username = "foo"
        logging.info(f"*** test_get_by_user_username path {username}")

        response = await http_client(TEST_URL, "/users/foo")
        actual_result = response.fetchall()

        logging.info(f"*** test_get_by_user_username {actual_result}")

        assert len(actual_result) == 1
        assert actual_result[0].username == "foo"

    async def test_get_users(self):
        response = await http_client(TEST_URL, "/users")

        actual_result = response.json()
        logging.info(f"*** test_get_users {actual_result}")

        assert len(actual_result) == 1
        assert actual_result[0].username == "foo"

    # async def test_post_user(self):
    #     logging.info(f"*** test_post_user")
    #
    #     user = User(username="hi", password_hash="ho", salt="he", enabled=True)
    #
    #     self.db_conn.add_all([user])
    #     await self.db_conn.commit()
    #
    #
    #     logging.info(f"*** TEST results {actual_result}")
    #     assert actual_result.length == 1
    # TODO use the result endpoint - create them first...
    # async def test_post_user(self):
    #     logging.info(f"*** test_post_user")
    #
    #     user = User(username="hi", password_hash="ho", salt="he", enabled=True)
    #
    #     self.db_conn.add_all([user])
    #     await self.db_conn.commit()
    #
    #     results = await get_users(self.db_conn)
    #     actual_result = results.fetchall()
    #     logging.info(f"*** TEST results {actual_result}")
    #     assert actual_result.length == 1

    #     self.db_conn.add_all([user])

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
