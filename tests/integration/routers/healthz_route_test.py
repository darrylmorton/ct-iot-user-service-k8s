from tests.helper.routes import TEST_URL, http_client


async def test_healthz():
    expected_result = {"message": "ok"}

    response = await http_client(TEST_URL, "/healthz")
    actual_result = response.json()

    assert response.status_code == 200
    assert actual_result == expected_result
