import config
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


async def test_healthz():
    expected_result = {"message": "ok", "version": config.APP_VERSION}

    response = await RoutesHelper.http_client(app, "/healthz")
    actual_result = response.json()

    assert response.status_code == 200
    assert actual_result == expected_result
