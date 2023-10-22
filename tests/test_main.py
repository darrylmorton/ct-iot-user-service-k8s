import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.anyio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
