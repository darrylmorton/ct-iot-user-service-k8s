import pytest

from tests.helper.user_helper import create_signup_payload
from tests.helper.auth_helper import create_token
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestUsersRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = "foo@home.com"
    password = "barbarba"
    admin = False
    token = create_token(data={"id": id, "is_admin": admin})

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=True)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token(self, db_cleanup, add_test_user):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result["id"] == self.id

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_enabled=False)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token_user_not_enabled(
        self, db_cleanup, add_test_user
    ):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        assert response.status_code == 401
