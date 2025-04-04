import pytest

from tests.helper.user_helper import create_signup_payload
from tests.helper.token_helper import create_token_expiry, create_token
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app
import tests.config as test_config


# Only testing unhappy paths
# Corresponding router happy paths are tested via other router tests
class TestMiddlewareAuthorise:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    is_admin = True
    password = "barbarba"

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_not_admin_different_id(self, db_cleanup, add_test_user):
        _token = create_token(
            secret=test_config.JWT_SECRET, data={"id": self._id, "is_admin": False}
        )

        response = await RoutesHelper.http_client(
            app, "/api/users/eaf0bb67-288b-4e56-860d-e727b4f57ff9", _token
        )

        actual_result = response.json()

        assert response.status_code == 403
        assert actual_result == "Forbidden error"

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_not_admin(self, db_cleanup, add_test_user):
        _token = create_token(
            secret=test_config.JWT_SECRET, data={"id": self._id, "is_admin": False}
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
        assert actual_result["message"] == "Unauthorised error"

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_expired_token(self, db_cleanup, add_test_user):
        _token = create_token(
            secret=test_config.JWT_SECRET,
            data={"id": self._id, "is_admin": self.is_admin},
            expiry=create_token_expiry(-3000),
        )

        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"

    async def test_invalid_token(self):
        _token = create_token(
            secret=test_config.JWT_SECRET,
            data={"id": self._id, "is_admin": self.is_admin},
        )

        response = await RoutesHelper.http_client(app, "/api/admin/users", _token)
        actual_result = response.json()

        assert response.status_code == 401
        assert actual_result == "Unauthorised error"
