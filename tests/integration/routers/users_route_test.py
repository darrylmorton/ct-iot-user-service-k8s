from unittest import skip

import pytest
from jose import jwt

from tests.helper.user_helper import create_signup_payload
import tests.config as tests_config
from tests.helper.auth_helper import create_token_expiry
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app
from utils.app_util import AppUtil


class TestUsersRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = "foo@home.com"
    password = "barbarba"
    admin = False

    token = jwt.encode(
        {"id": id, "admin": admin, "exp": create_token_expiry()},
        tests_config.JWT_SECRET,
        algorithm="HS256",
    )

    @skip(reason="requires user roles")
    async def test_get_users(self):
        response = await RoutesHelper.http_client(app, "/api/admin/users", self.token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 1
        assert AppUtil.validate_uuid4(actual_result[0]["id"])
        assert actual_result[0]["username"] == self.username

    @skip(reason="requires user roles")
    async def test_get_users_offset(self):
        response = await RoutesHelper.http_client(
            app, "/api/admin/users?offset=1", self.token
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 0

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=True)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token(self, db_cleanup, add_test_user):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        actual_result = response.json()

        assert response.status_code == 200
        assert AppUtil.validate_uuid4(actual_result["id"])
        assert actual_result["username"] == self.username

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=False)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token_user_not_enabled(
        self, db_cleanup, add_test_user
    ):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        assert response.status_code == 401
