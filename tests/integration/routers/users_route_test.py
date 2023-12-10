import json
import logging

from tests.helper.routes import http_client, TEST_URL, http_post_client


# TODO return id and username from save result...
async def test_post_user(db_cleanup):
    username = "foo"
    payload = json.dumps({"username": username, "password": "bar"})

    response = await http_post_client(TEST_URL, "/api/users", payload)
    actual_result = response.json()

    logging.info("*** *** *** result", actual_result)

    assert type(actual_result["id"]) is int
    assert actual_result["username"] == username
    assert response.status_code == 201


async def test_get_users():
    expected_result = "foo"

    response = await http_client(TEST_URL, "/api/users")
    actual_result = response.json()

    assert len(actual_result) == 1
    assert type(actual_result[0]["id"]) is int
    assert actual_result[0]["username"] == expected_result


async def test_get_by_user_username():
    expected_result = "foo"

    response = await http_client(TEST_URL, f"/api/users/{expected_result}")
    actual_result = response.json()

    assert len(actual_result) == 1
    assert type(actual_result[0]["id"]) is int
    assert actual_result[0]["username"] == expected_result
