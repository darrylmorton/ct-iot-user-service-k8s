import datetime
import json
from unittest.mock import MagicMock, patch

import jwt
import pytest
from fastapi import HTTPException
from jwt import ExpiredSignatureError

from src.config import JWT_SECRET
from ...helper.routes import TEST_URL, http_post_client


async def test_post_signup_invalid_username():
    username = "foo"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 400


async def test_post_signup_invalid_password():
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarb"})

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 400


async def test_post_signup(db_cleanup):
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/signup", payload)
    actual_result = response.json()

    assert response.status_code == 201
    assert type(actual_result["id"]) is int
    assert actual_result["username"] == username


async def test_post_signup_user_exists():
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 409


async def test_post_login_invalid_username():
    username = "foo"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/login", payload)

    assert response.status_code == 401


async def test_post_login_invalid_password():
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarb"})

    response = await http_post_client(TEST_URL, "/api/login", payload)

    assert response.status_code == 401


async def test_post_login(db_cleanup):
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})

    await http_post_client(TEST_URL, "/api/signup", payload)
    response = await http_post_client(TEST_URL, "/api/login", payload)
    response_json = response.json()

    actual_result = jwt.decode(response_json["token"], JWT_SECRET, algorithms=["HS256"])

    assert response.status_code == 200
    assert actual_result["username"] == username


@patch("src.utils.date_util.create_token_expiry")
async def test_post_login_expired_token(mock_function, db_cleanup):
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})
    error_message = "login expired signature error"

    await http_post_client(TEST_URL, "/api/signup", payload)
    # (datetime.datetime.now(
    #             tz=datetime.timezone.utc) +
    #          datetime.timedelta(seconds=-30))

    mock_function.return_value = MagicMock(
        return_value=(
            datetime.datetime.now(tz=datetime.timezone.utc)
            - datetime.timedelta(seconds=3000)
        )
    )

    with pytest.raises(HTTPException) as error:
        # try:
        response = await http_post_client(TEST_URL, "/api/login", payload)
        result = response.json()

        # actual_result = jwt.decode(result["token"], JWT_SECRET, algorithms=["HS256"])

    assert error.errisinstance(HTTPException)
    assert result.status_code == 401
    assert error.value.detail == error_message

    # assert actual_result["username"] == username


# try:
#     jwt.decode("JWT_STRING", "secret", algorithms=["HS256"])
# except jwt.ExpiredSignatureError:
#     # Signature has expired
#     ...
