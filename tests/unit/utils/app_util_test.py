from unittest import skip

from utils.app_util import AppUtil
from utils.validator_util import ValidatorUtil


class TestAppUtil:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"

    def test_validate_uuid4(self):
        actual_result = ValidatorUtil.validate_uuid4(self._id)

        assert actual_result is True

    def test_validate_uuid4_invalid_uuid(self):
        actual_result = ValidatorUtil.validate_uuid4("848a3cdd")

        assert actual_result is False

    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "1.0.3"

    @skip
    def test_create_db_url_suffix(self):
        pass

    @skip
    def test_get_alembic_db_url(self):
        pass

    @skip
    def test_get_sqlalchemy_db_url(self):
        pass
