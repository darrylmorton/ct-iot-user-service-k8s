from httpx import AsyncClient

TEST_URL = "http://localhost:8001"


async def http_client(base_url, path, token=None):
    # path = urllib.parse.unquote(path)

    async with AsyncClient(base_url=base_url) as ac:
        if token:
            ac.headers["Authorization"] = token
        return await ac.get(path)


async def http_post_client(base_url, path, payload, token=None):
    async with AsyncClient(base_url=base_url) as ac:
        if token:
            ac.headers["Authorization"] = token
        return await ac.post(path, json=payload)


async def mock_http_client(app, base_url, path):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        return await ac.get(path)
