import pytest
from jose import jwt

from tests.config import JWT_SECRET
from tests.helper.auth_helper import create_token_expiry
from tests.helper.routes_helper import http_client, TEST_URL

username = "foo@home.com"
password = "barbarba"


@pytest.mark.skip
class TestAuthorise:
    async def test_authorise_invalid_request(self):
        _token = ""
        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Invalid key error"

    async def test_authorise_expired_token(self):
        _token = jwt.encode(
            {"username": username, "exp": create_token_expiry(-3000)},
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Expired token error"

    async def test_authorise_invalid_token(self):
        _token = jwt.encode(
            {"username": username, "exp": create_token_expiry(-3000)},
            "",
            algorithm="HS256",
        )

        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Invalid token error"
