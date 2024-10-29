from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database.admin_crud import AdminCrud
from database.user_crud import UserCrud
from database.user_details_crud import UserDetailsCrud


class TestCrudExceptions:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    user_id = "00000000-0000-0000-0000-000000000000"
    username = "foo@home.com"
    password = "barbarba"
    first_name = "Foo"
    last_name = "Bar"

    @pytest.mark.skip
    @patch("database.admin_crud_stmt.AdminCrudStmt.find_users_stmt")
    async def test_find_users_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await AdminCrud().find_users()

    @patch("database.user_crud_stmt.UserCrudStmt.find_user_by_id_stmt")
    async def test_find_user_by_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await UserCrud().find_user_by_id(self.id)

    @patch("database.user_crud_stmt.UserCrudStmt.find_user_by_username_stmt")
    async def test_find_user_by_username_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await UserCrud().find_user_by_username(self.username)

    @patch("database.user_crud_stmt.UserCrudStmt.add_user_model")
    async def test_add_user_exception(self, mock_model):
        mock_model.return_value = None

        with pytest.raises(SQLAlchemyError):
            await UserCrud().add_user(self.username, self.password)

    @patch(
        "database.user_details_crud_stmt.UserDetailsCrudStmt.find_user_details_by_user_id_stmt"
    )
    async def test_find_user_details_by_user_id_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await UserDetailsCrud().find_user_details_by_user_id(self.user_id)

    @patch("database.user_details_crud_stmt.UserDetailsCrudStmt.add_user_details_model")
    async def test_add_user_details_model_exception(self, mock_stmt):
        mock_stmt.return_value = None

        with pytest.raises(SQLAlchemyError):
            await UserDetailsCrud().add_user_details(
                self.user_id, self.first_name, self.last_name
            )
