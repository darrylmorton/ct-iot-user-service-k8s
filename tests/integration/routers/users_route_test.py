from jose import jwt

from src.config import JWT_SECRET
from src.utils.auth_util import create_token_expiry
from ...helper.routes_helper import http_client, TEST_URL

username = "foo@home.com"
password = "barbarba"

token = jwt.encode(
    {"username": username, "exp": create_token_expiry()},
    JWT_SECRET,
    algorithm="HS256",
)


class TestUsersRoute:
    async def test_get_users_valid_token(self):
        response = await http_client(TEST_URL, "/api/users", token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 1
        assert type(actual_result[0]["id"]) is int
        assert actual_result[0]["username"] == username

    async def test_get_users(self):
        response = await http_client(TEST_URL, "/api/users", token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 1
        assert type(actual_result[0]["id"]) is int
        assert actual_result[0]["username"] == username

    async def test_get_users_offset(self):
        response = await http_client(TEST_URL, "/api/users?offset=1", token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 0

    async def test_get_by_user_username(self):
        response = await http_client(TEST_URL, f"/api/users/{username}", token)
        actual_result = response.json()

        assert response.status_code == 200
        assert type(actual_result["id"]) is int
        assert actual_result["username"] == username
