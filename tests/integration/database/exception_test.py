from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

import crud


class TestCrudExceptions:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    user_id = "00000000-0000-0000-0000-000000000000"
    username = "foo@home.com"
    password = "barbarba"
    first_name = "Foo"
    last_name = "Bar"

    @pytest.mark.skip
    @patch("utils.db_util.find_users_stmt")
    async def test_find_users_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_users()

    @patch("utils.db_util.find_user_by_id_stmt")
    async def test_find_user_by_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_user_by_id(self.id)

    @patch("utils.db_util.find_user_by_id_and_enabled_stmt")
    async def test_find_user_by_id__and_enabled_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_user_by_id_and_enabled(self.id)

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

    @patch("utils.db_util.find_user_details_stmt")
    async def test_find_user_details_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_user_details()

    @patch("utils.db_util.find_user_details_by_user_id_stmt")
    async def test_find_user_details_by_user_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.find_user_details_by_user_id(self.user_id)

    @patch("utils.db_util.add_user_details_model")
    async def test_add_user_details_model_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await crud.add_user_details(self.user_id, self.first_name, self.last_name)
