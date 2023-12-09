import json
import logging

from tests.helper.routes import http_client, TEST_URL, http_post_client


async def test_post_user(db_cleanup):
    payload = json.dumps({"username": "foo2", "password": "bar2"})

    response = await http_post_client(TEST_URL, "/api/users", payload)
    actual_result = response.json()

    assert actual_result["username"] == "foo2"
    assert response.status_code == 201


async def test_get_users():
    expected_username = "foo2"

    response = await http_client(TEST_URL, "/api/users")
    actual_result = response.json()
    logging.info(f"*** test_get_users {actual_result}")

    assert len(actual_result) == 1
    assert actual_result[0]["username"] == expected_username


async def test_get_by_user_username():
    expected_username = "foo2"

    response = await http_client(TEST_URL, f"/api/users/{expected_username}")
    actual_result = response.json()

    assert len(actual_result) == 1
    assert actual_result[0]["username"] == expected_username
