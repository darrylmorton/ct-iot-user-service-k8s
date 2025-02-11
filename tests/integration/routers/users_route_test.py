import pytest

import tests.config as test_config
from tests.helper.user_helper import create_signup_payload
from tests.helper.token_helper import create_token
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestUsersRoute:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    username = test_config.USERNAME
    password = "barbarba"
    is_admin = False
    token = create_token(
        secret=test_config.JWT_SECRET, data={"id": id, "is_admin": is_admin}
    )

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True)]],
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
        [[create_signup_payload(_confirmed=True)]],
        indirect=True,
    )
    async def test_get_by_user_id_invalid_uuid(self, db_cleanup, add_test_user):
        response = await RoutesHelper.http_client(
            app, "/api/users/848a3cdd-cafd-4ec6-a921-afb0bcc841d", self.token
        )

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=False)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token_user_unconfirmed(
        self, db_cleanup, add_test_user
    ):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True, _enabled=False)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token_user_suspended(
        self, db_cleanup, add_test_user
    ):
        response = await RoutesHelper.http_client(
            app, f"/api/users/{self.id}", self.token
        )

        assert response.status_code == 403

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload(_confirmed=True, _enabled=False)]],
        indirect=True,
    )
    async def test_get_by_user_id_valid_token_user_does_not_exist(
        self, db_cleanup, add_test_user
    ):
        token = create_token(
            secret=test_config.JWT_SECRET,
            data={
                "id": "848a3cdd-cafd-4ec6-a921-afb0bcc841de",
                "is_admin": self.is_admin,
            },
        )

        response = await RoutesHelper.http_client(app, f"/api/users/{self.id}", token)

        assert response.status_code == 401
