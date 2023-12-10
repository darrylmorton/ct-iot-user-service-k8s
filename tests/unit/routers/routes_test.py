from src.main import server
from ...helper.routes import mock_http_client


async def test_health():
    response = await mock_http_client(server, "http://test", "healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
