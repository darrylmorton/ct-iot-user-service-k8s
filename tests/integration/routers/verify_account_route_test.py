import pytest

import tests.config as test_config
from tests.helper.token_helper import create_token
from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestVerifyAccountRoute:
    token = create_token(
        secret=test_config.JWT_SECRET_VERIFY_ACCOUNT,
        data={
            "username": test_config.USERNAME,
            "email_type": test_config.EMAIL_ACCOUNT_VERIFICATION_TYPE,
        },
    )

    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload()]],
        indirect=True,
    )
    async def test_verify_account(self, db_cleanup, add_test_user):
        response = await RoutesHelper.http_client(
            app, f"/api/verify-account/?token={self.token}"
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result == "Account confirmed"

    async def test_verify_account_user_does_not_exist(self, db_cleanup):
        response = await RoutesHelper.http_client(
            app, f"/api/verify-account/?token={self.token}"
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result == ""

    async def test_verify_account_no_token(self, db_cleanup):
        response = await RoutesHelper.http_client(app, "/api/verify-account/?token=")

        assert response.status_code == 400
