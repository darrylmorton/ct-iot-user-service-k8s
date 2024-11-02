from unittest import skip

from tests.helper.routes_helper import RoutesHelper
from tests.helper.user_helper import create_signup_payload
from user_service.service import app


class TestAccountConfirmationRoute:
    @skip
    async def test_post_account_confirmation(self, db_cleanup):
        payload = create_signup_payload()

        await RoutesHelper.http_post_client(app, "/api/signup", payload)

        # assert response.status_code == 201
        # assert response.json()["username"] == tests.config.TEST_USERNAME

        await RoutesHelper.http_client(app, "/api/account-confirmation/?token=blah")
