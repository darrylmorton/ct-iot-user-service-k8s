import pytest
from jose import jwt

from tests.helper.user_helper import create_signup_payload
from tests.config import JWT_SECRET
from tests.helper.auth_helper import create_token_expiry
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


# Only testing unhappy paths
# Corresponding router happy paths are tested via other router tests
class TestMiddlewareAuthorise:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    admin = True
    password = "barbarba"

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=True)]],
        indirect=True,
    )
    async def test_not_admin_different_id(self, db_cleanup, add_test_user):
        _token = jwt.encode(
            {"id": self._id, "is_admin": False, "exp": create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(
            app, "/api/users/eaf0bb67-288b-4e56-860d-e727b4f57ff9", _token
        )
        actual_result = response.json()

        assert response.status_code == 403
        assert actual_result == "Forbidden error"

    async def test_not_admin(self):
        _token = jwt.encode(
            {"id": self._id, "is_admin": False, "exp": create_token_expiry()},
            JWT_SECRET,
            algorithm="HS256",
        )
        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 403
        assert actual_result == "Forbidden error"

    async def test_missing_token(self):
        _token = ""
        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"

    async def test_expired_token(self):
        _token = jwt.encode(
            {"id": self._id, "is_admin": self.admin, "exp": create_token_expiry(-3000)},
            JWT_SECRET,
            algorithm="HS256",
        )

        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"

    async def test_invalid_token(self):
        _token = jwt.encode(
            {"id": self._id, "is_admin": self.admin, "exp": create_token_expiry()},
            "",
            algorithm="HS256",
        )

        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"
