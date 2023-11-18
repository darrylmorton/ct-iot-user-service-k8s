import logging
import pytest

from tests.helper.db import cleanup
from src.database import SessionLocal
from src.models import User

from tests.helper.routes import http_client, TEST_URL

LOGGER = logging.getLogger("user-service")

db = SessionLocal()


@pytest.mark.anyio
async def before_all():
    await cleanup()


@pytest.mark.anyio
async def test_health():
    response = await http_client(TEST_URL, "/healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


@pytest.mark.anyio
async def test_post_user():
    user = (User(username="hi", password_hash="ho", salt="he", enabled=True))

    db.add_all([user])
    db.commit()
