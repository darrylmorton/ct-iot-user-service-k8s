from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app

username = "foo@home.com"
password = "barbarba"
first_name = "Foo"
last_name = "Bar"


class TestSignupRoute:
    async def test_post_signup_invalid_username(self):
        _username = "foo"
        payload = create_signup_payload(_username=_username)

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 422

    async def test_post_signup_invalid_password(self):
        payload = create_signup_payload(_password="barbarb")

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 422

    async def test_post_signup(self, db_cleanup):
        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)
        actual_result = response.json()

        assert response.status_code == 201
        assert actual_result["username"] == username

    async def test_post_signup_user_exists(self):
        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 409
