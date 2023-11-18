import pytest

from src.main import app
from tests.helper.routes import mock_http_client


@pytest.mark.anyio
async def test_health():
    response = await mock_http_client(app, "http://test", "healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
