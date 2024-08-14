from utils.app_util import AppUtil


class TestAppUtil:
    def test_validate_uuid4(self):
        actual_result = AppUtil.validate_uuid4("848a3cdd-cafd-4ec6-a921-afb0bcc841dd")

        assert actual_result is True

    def test_validate_uuid4_invalid_uuid(self):
        actual_result = AppUtil.validate_uuid4("848a3cdd")

        assert actual_result is False

    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "1.0.1"
