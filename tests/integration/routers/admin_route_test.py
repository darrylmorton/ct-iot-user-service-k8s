from unittest import skip

import pytest
from jose import jwt

from tests.helper.user_helper import create_signup_payload
import tests.config as tests_config
from tests.helper.token_helper import create_token_expiry
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestAdminRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = tests_config.USERNAME
    password = "barbarba"
    is_admin = True

    token = jwt.encode(
        {"id": id, "is_admin": is_admin, "exp": create_token_expiry()},
        tests_config.JWT_SECRET,
        algorithm="HS256",
    )

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True, _is_admin=True)]],
        indirect=True,
    )
    async def test_get_users(self, db_cleanup, add_test_user):
        response = await RoutesHelper.http_client(app, "/api/admin/users", self.token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 1
        assert actual_result[0]["id"] == self.id
        assert actual_result[0]["username"] == self.username

    @skip(reason="requires full pagination")
    async def test_get_users_offset(self):
        response = await RoutesHelper.http_client(
            app, "/api/admin/users?offset=1", self.token
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 0

    @skip(reason="Not implemented yet")
    async def test_pagination(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_creates_user(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_disables_user(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_enables_user(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_updates_another_user(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_updates_another_user_to_admin(self):
        pass

    @skip(reason="Not implemented yet")
    async def test_admin_updates_another_admin_to_user(self):
        pass
