import pytest

import tests.config as test_config
from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app
from utils.token_util import TokenUtil


class TestVerifyAccountRoute:
    @pytest.mark.parametrize(
        "add_test_user",
        [[create_signup_payload()]],
        indirect=True,
    )
    async def test_verify_account(self, db_cleanup, add_test_user):
        token = TokenUtil.encode_token(
            test_config.SES_TARGET, test_config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE
        )

        response = await RoutesHelper.http_client(
            app, f"/api/verify-account/?token={token}"
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result == "Account confirmed"

    async def test_verify_account_user_does_not_exist(self, db_cleanup):
        token = TokenUtil.encode_token(
            test_config.SES_TARGET, test_config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE
        )

        response = await RoutesHelper.http_client(
            app, f"/api/verify-account/?token={token}"
        )
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result == ""

    async def test_verify_account_no_token(self, db_cleanup):
        response = await RoutesHelper.http_client(app, f"/api/verify-account/?token=")

        assert response.status_code == 400
