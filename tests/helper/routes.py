from httpx import AsyncClient

TEST_URL = "http://localhost:8001"


async def http_client(base_url, path):
    # path = urllib.parse.unquote(path)

    async with AsyncClient(base_url=base_url) as ac:
        return await ac.get(path)


async def http_post_client(base_url, path, payload):
    async with AsyncClient(base_url=base_url) as ac:
        return await ac.post(path, json=payload)


# async def http_client_with_path(base_url, path):
#     path = urllib.parse.unquote(path)
#
#     async with AsyncClient(base_url=base_url) as ac:
#         return await ac.get(path)


async def mock_http_client(app, base_url, path):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        return await ac.get(path)
