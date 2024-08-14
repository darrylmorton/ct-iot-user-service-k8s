from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from crud import Crud


class TestCrudExceptions:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    user_id = "00000000-0000-0000-0000-000000000000"
    username = "foo@home.com"
    password = "barbarba"
    first_name = "Foo"
    last_name = "Bar"

    @pytest.mark.skip
    @patch("crud_stmt.CrudStmt.find_users_stmt")
    async def test_find_users_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_users()

    @patch("crud_stmt.CrudStmt.find_user_by_id_stmt")
    async def test_find_user_by_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_user_by_id(self.id)

    @patch("crud_stmt.CrudStmt.find_user_by_id_and_enabled_stmt")
    async def test_find_user_by_id__and_enabled_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_user_by_id_and_enabled(self.id)

    @patch("crud_stmt.CrudStmt.find_user_by_username_stmt")
    async def test_find_user_by_username_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_user_by_username(self.username)

    @patch("crud_stmt.CrudStmt.add_user_model")
    async def test_add_user_exception(self, mock_model):
        mock_model.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().add_user(self.username, self.password)

    @patch("crud_stmt.CrudStmt.find_user_details_stmt")
    async def test_find_user_details_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_user_details()

    @patch("crud_stmt.CrudStmt.find_user_details_by_user_id_stmt")
    async def test_find_user_details_by_user_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().find_user_details_by_user_id(self.user_id)

    @patch("crud_stmt.CrudStmt.add_user_details_model")
    async def test_add_user_details_model_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await Crud().add_user_details(self.user_id, self.first_name, self.last_name)
