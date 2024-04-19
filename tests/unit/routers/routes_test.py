from user_service.service import server
from tests.helper.routes_helper import mock_http_client


async def test_health():
    response = await mock_http_client(server, "http://test", "healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
