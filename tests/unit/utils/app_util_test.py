from utils import app_util


class TestAppUtil:
    def test_validate_uuid4(self):
        actual_result = app_util.validate_uuid4("848a3cdd-cafd-4ec6-a921-afb0bcc841dd")

        assert actual_result is True

    def test_validate_uuid4_invalid_uuid(self):
        actual_result = app_util.validate_uuid4("848a3cdd")

        assert actual_result is False
