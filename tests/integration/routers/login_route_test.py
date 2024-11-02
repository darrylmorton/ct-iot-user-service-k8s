import pytest
from jose import jwt

import tests.config
from tests.config import JWT_SECRET
from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestLoginRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = tests.config.SES_TARGET

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
        [[create_signup_payload(_confirmed=False)]],
        indirect=True,
    )
    async def test_post_login_user_unconfirmed(self, db_cleanup, add_test_user):
        payload = create_signup_payload(_confirmed=False)

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True, _enabled=False)]],
        indirect=True,
    )
    async def test_post_login_user_suspended(self, db_cleanup, add_test_user):
        payload = create_signup_payload(_confirmed=True, _enabled=False)

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 403

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_post_login_user_does_not_exist(self, db_cleanup, add_test_user):
        payload = create_signup_payload(_username="bar@home.com", _confirmed=True)

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_post_login_user(self, db_cleanup, add_test_user):
        payload = create_signup_payload(_confirmed=True)

        response = await RoutesHelper.http_post_client(app, "/api/login", payload)
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["id"] == self.id
