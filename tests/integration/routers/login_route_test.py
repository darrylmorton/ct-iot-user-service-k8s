import pytest
from jose import jwt

from tests.config import JWT_SECRET
from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestLoginRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = "foo@home.com"

    async def test_post_login_invalid_username(self):
        _username = "foo"
        payload = create_signup_payload(_username)

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 401

    async def test_post_login_invalid_password(self):
        payload = create_signup_payload(_password="barbarb")

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload()]],
        indirect=True,
    )
    async def test_post_login_user_not_enabled(self, db_cleanup, add_test_user):
        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 403

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=True)]],
        indirect=True,
    )
    async def test_post_login_user(self, db_cleanup, add_test_user):
        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["id"] == self.id
