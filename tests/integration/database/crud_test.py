from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from crud import find_users, find_user_by_username


class TestCrud:
    username = "foo@home.com"

    async def test_find_users(self):
        result = await find_users()

        assert len(result) == 0

    @patch("utils.db_util.find_users_stmt")
    async def test_find_users_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await find_users()

    async def test_find_user_by_username(self):
        result = await find_user_by_username(self.username)

        assert not result

    @patch("utils.db_util.find_user_by_username_stmt")
    async def test_find_user_by_username_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await find_user_by_username(self.username)
