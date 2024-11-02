import asyncio
import os
from uuid import UUID
import boto3
from dotenv import load_dotenv
from moto import mock_aws

import bcrypt
import pytest
from sqlalchemy import delete

from database.models import UserModel, UserDetailsModel
from logger import log
from sqs.email_producer import EmailProducer
from tests.database import async_session
from tests.config import AWS_REGION, SES_SOURCE

load_dotenv(dotenv_path=".env.test")


@pytest.fixture
def aws_credentials():
    # Mocked AWS Credentials for moto
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION"] = AWS_REGION


@pytest.fixture
def ses_client(aws_credentials):
    with mock_aws():
        conn = boto3.client("ses", region_name=AWS_REGION)

        response = conn.verify_email_identity(EmailAddress=SES_SOURCE)
        log.debug(f"***** RESPONSE {response=}")

        yield conn


@pytest.fixture
def email_producer(ses_client):
    producer = EmailProducer()

    yield producer


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_cleanup():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(UserDetailsModel))
            await session.execute(delete(UserModel))
            await session.commit()
            await session.close()


@pytest.fixture
async def add_test_user(request):
    user_request = request.param[0]

    password = user_request["password"].encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

    user = UserModel(
        id=UUID("848a3cdd-cafd-4ec6-a921-afb0bcc841dd"),
        username=user_request["username"],
        password_hash=password_hash,
        confirmed=user_request["confirmed"],
        enabled=user_request["enabled"],
        is_admin=user_request["is_admin"],
    )

    async with async_session() as session:
        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

    return {
        "id": user.id,
        "username": user.username,
        "confirmed": user.confirmed,
        "enabled": user.enabled,
        "first_name": user_request["first_name"],
        "last_name": user_request["last_name"],
    }
