import json

from ...helper.routes import http_client, TEST_URL, http_post_client


async def test_post_user_invalid_username():
    username = "foo"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/users", payload)

    assert response.status_code == 400


async def test_post_user_invalid_password():
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarb"})

    response = await http_post_client(TEST_URL, "/api/users", payload)

    assert response.status_code == 400


async def test_post_user(db_cleanup):
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/users", payload)
    actual_result = response.json()

    assert response.status_code == 201
    assert type(actual_result["id"]) is int
    assert actual_result["username"] == username


async def test_post_user_exists():
    username = "foo@home.com"
    payload = json.dumps({"username": username, "password": "barbarba"})

    response = await http_post_client(TEST_URL, "/api/users", payload)

    assert response.status_code == 409


async def test_get_users():
    expected_result = "foo@home.com"

    response = await http_client(TEST_URL, "/api/users")
    actual_result = response.json()

    assert response.status_code == 200
    assert len(actual_result) == 1
    assert type(actual_result[0]["id"]) is int
    assert actual_result[0]["username"] == expected_result


async def test_get_users_offset():
    response = await http_client(TEST_URL, "/api/users?offset=1")
    actual_result = response.json()

    assert response.status_code == 200
    assert len(actual_result) == 0


async def test_get_by_user_username():
    expected_result = "foo@home.com"

    response = await http_client(TEST_URL, f"/api/users/{expected_result}")
    actual_result = response.json()

    assert response.status_code == 200
    assert type(actual_result["id"]) is int
    assert actual_result["username"] == expected_result
