# # import logging
# #
# # import pytest
# # from sqlalchemy import delete
# # from sqlalchemy.ext.asyncio import AsyncSession
# #
# # from tests.helper.db import AsyncSessionLocal
# # from src.models import User
# #
# #
# # # @pytest.mark.asyncio
# # @pytest.fixture  # (autouse=True)
# # async def my_before_all():
# #     logging.info(f"*** TEST BEFORE_ALL CALLED!")
# #
# #     db_conn = AsyncSessionLocal()
# #     # await cleanup(db)
# #     await db_conn.execute(delete(User))
# #     await db_conn.commit()
# #
# #     # await db_conn.close()
# import unittest
# from unittest import IsolatedAsyncioTestCase
#
# from sqlalchemy import delete
#
# from src.models import User
# from tests.helper.db import AsyncSessionLocal
#
# events = []
#
#
# class MyTest(unittest.IsolatedAsyncioTestCase):
#
#     # def setUp(self):
#     #     events.append("setUp")
#
#     async def asyncSetUp(self):
#         self._async_connection = AsyncSessionLocal()
#         events.append("asyncSetUp")
#
#     # async def test_response(self):
#     #     events.append("test_response")
#     #     response = await self._async_connection.get("https://example.com")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.addAsyncCleanup(self.on_cleanup)
#
#     # def tearDown(self):
#     #     events.append("tearDown")
#
#     async def asyncTearDown(self):
#         await self._async_connection.execute(delete(User))
#         # await self._async_connection.close()
#         events.append("asyncTearDown")
#
#
#     async def on_cleanup(self):
#         events.append("cleanup")
#
#
# if __name__ == "__main__":
#     unittest.main()
