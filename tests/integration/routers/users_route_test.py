from jose import jwt

from tests.config import JWT_SECRET
from tests.helper.auth_helper import create_token_expiry
from tests.helper.routes_helper import http_client, TEST_URL, validate_uuid4

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
        assert validate_uuid4(actual_result[0]["id"])
        assert actual_result[0]["username"] == username

    async def test_get_users(self):
        response = await http_client(TEST_URL, "/api/users", token)
        actual_result = response.json()

        assert response.status_code == 200
        assert len(actual_result) == 1
        assert validate_uuid4(actual_result[0]["id"])
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
        assert validate_uuid4(actual_result["id"])
        assert actual_result["username"] == username
