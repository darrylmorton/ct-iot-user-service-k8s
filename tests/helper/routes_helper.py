import uuid

from httpx import AsyncClient

from tests.config import APP_HOST, APP_PORT


TEST_URL = f"http://{APP_HOST}:{APP_PORT}"


async def http_client(base_url, path, token=None):
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


def validate_uuid4(uuid_string) -> bool:
    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = uuid.UUID(uuid_string, version=4)

    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return str(val) == uuid_string
