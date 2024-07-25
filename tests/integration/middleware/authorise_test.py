import pytest
from jose import jwt

from tests.config import JWT_SECRET
from tests.helper.auth_helper import create_token_expiry
from tests.helper.routes_helper import http_client, TEST_URL


@pytest.mark.skip(reason="Users not implemented yet")
class TestAuthorise:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = "foo@home.com"
    password = "barbarba"

    async def test_authorise_invalid_request(self):
        _token = ""
        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Invalid key error"

    async def test_authorise_expired_token(self):
        _token = jwt.encode(
            {"id": self._id, "exp": create_token_expiry(-3000)},
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"

    async def test_authorise_invalid_token(self):
        _token = jwt.encode(
            {"id": self._id, "exp": create_token_expiry(-3000)},
            "",
            algorithm="HS256",
        )

        response = await http_client(TEST_URL, "/api/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"
