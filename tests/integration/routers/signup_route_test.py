import pytest
from jose import jwt

from src.config import JWT_SECRET
from ...helper.user_helper import create_signup_payload, create_login_payload
from ...helper.routes_helper import TEST_URL, http_post_client

username = "foo@home.com"
password = "barbarba"
first_name = "Foo"
last_name = "Bar"


class TestAuthRoute:
    async def test_post_signup_invalid_username(self):
        _username = "foo"
        payload = create_signup_payload(_username=_username)

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 422

    async def test_post_signup_invalid_password(self):
        payload = create_signup_payload(_password="barbarb")

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 422

    async def test_post_signup(self, db_cleanup):
        payload = create_signup_payload()

        response = await http_post_client(TEST_URL, "/api/signup", payload)
        actual_result = response.json()

        assert response.status_code == 201
        assert actual_result["username"] == username

    async def test_post_signup_user_exists(self):
        payload = create_signup_payload()

        response = await http_post_client(TEST_URL, "/api/signup", payload)

        assert response.status_code == 409

    async def test_post_login_invalid_username(self):
        _username = "foo"
        payload = create_login_payload(_username)

        response = await http_post_client(TEST_URL, "/api/login", payload)

        assert response.status_code == 401

    async def test_post_login_invalid_password(self):
        payload = create_login_payload(_password="barbarb")

        response = await http_post_client(TEST_URL, "/api/login", payload)

        assert response.status_code == 401

    # @pytest.mark.skip
    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload()]],
        indirect=True,
    )
    async def test_post_login_user_not_enabled(self, db_cleanup, add_test_user):
        payload = create_login_payload()

        response = await http_post_client(TEST_URL, "/api/login", payload)

        assert response.status_code == 403

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=True)]],
        indirect=True,
    )
    async def test_post_login_user(self, db_cleanup, add_test_user):
        payload = create_login_payload()

        response = await http_post_client(TEST_URL, "/api/login", payload)
        response_json = response.json()

        actual_result = jwt.decode(
            response_json["token"], JWT_SECRET, algorithms=["HS256"]
        )

        assert response.status_code == 200
        assert actual_result["username"] == username
