# import datetime
# import json
# from unittest.mock import MagicMock, patch
import logging
from unittest.mock import patch, MagicMock

import jwt
import pytest

# from tests.conftest import add_test_user
# import pytest
# from fastapi import HTTPException
# from jwt import ExpiredSignatureError

from ...helper.user_helper import create_user_payload
from src.config import JWT_SECRET
from ...helper.routes_helper import TEST_URL, http_post_client


async def test_post_signup_invalid_username():
    username = "foo"
    payload = create_user_payload(username, "barbarba")

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 400


async def test_post_signup_invalid_password():
    username = "foo@home.com"
    payload = create_user_payload(username, "barbarb")

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 400


# async def test_post_signup_user_not_enabled(db_cleanup):
#     username = "foo@home.com"
#     password = "barbarba"
#     payload = create_user_payload(username, password)
#
#     # mock_function.return_value = MagicMock(await add_test_user(username, password))
#
#     response = await http_post_client(TEST_URL, "/api/signup", payload)
#     # actual_result = response.json()
#
#     assert response.status_code == 403


# @patch("src.routers.auth.add_user")
# async def test_post_signup_user_enabled(mock_function, db_cleanup):
#     username = "foo@home.com"
#     password = "barbarba"
#     payload = create_user_payload(username, password)
#
#     mock_function.return_value = MagicMock(await add_test_user(username, password))
#
#     response = await http_post_client(TEST_URL, "/api/signup", payload)
#     actual_result = response.json()
#
#     assert response.status_code == 201
#     assert type(actual_result["id"]) is int
#     assert actual_result["username"] == username

# async def test_post_signup(db_cleanup):
#     username = "foo@home.com"
#     payload = await add_test_user(create_user_payload(username,"barbarba")
#
#     response = await http_post_client(TEST_URL, "/api/signup", payload)
#     actual_result = response.json()
#
#     assert response.status_code == 201
#     assert type(actual_result["id"]) is int
#     assert actual_result["username"] == username


async def test_post_signup_user_exists():
    username = "foo@home.com"
    payload = create_user_payload(username, "barbarba")

    response = await http_post_client(TEST_URL, "/api/signup", payload)

    assert response.status_code == 409


async def test_post_login_invalid_username():
    username = "foo"
    payload = create_user_payload(username, "barbarba")

    response = await http_post_client(TEST_URL, "/api/login", payload)

    assert response.status_code == 401


async def test_post_login_invalid_password():
    username = "foo@home.com"
    payload = create_user_payload(username, "barbarb")

    response = await http_post_client(TEST_URL, "/api/login", payload)

    assert response.status_code == 401


@pytest.mark.parametrize('add_test_user', [[{
    "username": "foo@home.com",
    "password": "barbarba",
    "enabled": True
}]], indirect=True)
async def test_post_login_user(db_cleanup, add_test_user):
    username = "foo@home.com"
    password = "barbarba"
    payload = create_user_payload(username, password)

    response = await http_post_client(TEST_URL, "/api/login", payload)
    response_json = response.json()
    logging.info(f"response json {response_json}")
    actual_result = jwt.decode(response_json["token"], JWT_SECRET, algorithms=["HS256"])

    assert response.status_code == 200
    assert actual_result["username"] == username


# async def test_post_login_user_not_enabled(db_cleanup, add_test_user):
#     username = "foo@home.com"
#     password = "barbarba"
#     payload = create_user_payload(username, password)
#
#     # await http_post_client(TEST_URL, "/api/signup", payload)
#     await add_test_user(username, password)
#     response = await http_post_client(TEST_URL, "/api/login", payload)
#
#     assert response.status_code == 403


# @patch("src.routers.auth.create_token_expiry")
# async def test_post_login_expired_token(mock_function, db_cleanup):
#     username = "foo@home.com"
#     payload = json.dumps({"username": username, "password": "barbarba"})
#     error_message = "login expired signature error"
#
#     await http_post_client(TEST_URL, "/api/signup", payload)
#     # (datetime.datetime.now(
#     #             tz=datetime.timezone.utc) +
#     #          datetime.timedelta(seconds=-30))
#
#     mock_function.return_value = MagicMock(return_value=(
#         datetime.datetime.now(tz=datetime.timezone.utc)
#         + datetime.timedelta(hours=-24)
#     ))
#
#     with pytest.raises(HTTPException) as error:
#         response = await http_post_client(TEST_URL, "/api/login", payload)
#         result = response.json()
#
#         # actual_result = jwt.decode(result["token"], JWT_SECRET, algorithms=["HS256"])
#
#     assert error.errisinstance(HTTPException)
#     assert result.status_code == 401
#     assert error.value.detail == error_message

# assert actual_result["username"] == username


# try:
#     jwt.decode("JWT_STRING", "secret", algorithms=["HS256"])
# except jwt.ExpiredSignatureError:
#     # Signature has expired
#     ...
