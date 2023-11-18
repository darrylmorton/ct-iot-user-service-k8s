from httpx import AsyncClient

TEST_URL = "http://localhost:8001"


async def http_client(base_url, path):
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get(path)

        return response


async def mock_http_client(app, base_url, path):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(path)

        return response
