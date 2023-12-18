import logging
import pytest
from jose import jwt

from src.config import JWT_SECRET
from ...helper.user_helper import create_user_payload
from ...helper.routes_helper import TEST_URL, http_post_client

username = "foo@home.com"
password = "barbarba"


class TestAuthRoute:
    async def test_post_signup_invalid_username(self):
        _username = "foo"
        payload = create_user_payload(_username, password)

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 400

    async def test_post_signup_invalid_password(self):
        payload = create_user_payload(username, "barbarb")

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 400

    async def test_post_signup_user_exists(self):
        payload = create_user_payload()

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 409

    async def test_post_login_invalid_username(self):
        _username = "foo"
        payload = create_user_payload(_username, password)

        response = await http_post_client(TEST_URL, "/api/login", payload)

        assert response.status_code == 401

    async def test_post_login_invalid_password(self):
        payload = create_user_payload(username, "barbarb")

        response = await http_post_client(TEST_URL, "/api/login", payload)

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "add_test_user",
        [[{"username": username, "password": password, "enabled": True}]],
        indirect=True,
    )
    async def test_post_login_user(self, db_cleanup, add_test_user):
        payload = create_user_payload()

        response = await http_post_client(TEST_URL, "/api/login", payload)
        response_json = response.json()
        logging.info(f"response json {response_json}")

        actual_result = jwt.decode(
            response_json["token"], JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["username"] == username
