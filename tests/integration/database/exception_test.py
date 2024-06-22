from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

import crud


class TestCrudExceptions:
    username = "foo@home.com"
    password = "barbarba"

    @patch("utils.db_util.find_users_stmt")
    async def test_find_users_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_users()

    @patch("utils.db_util.find_user_by_username_stmt")
    async def test_find_user_by_username_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_user_by_username(self.username)

    @patch("utils.db_util.add_user_model")
    async def test_add_user_exception(self, mock_model):
        mock_model.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.add_user(self.username, self.password)
