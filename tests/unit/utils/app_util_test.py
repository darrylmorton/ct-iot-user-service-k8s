from unittest import skip
from unittest.mock import patch

import pytest

from utils.app_util import AppUtil
from utils.validator_util import ValidatorUtil


class TestAppUtil:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    _app_version = AppUtil.get_app_version()

    def test_validate_uuid4(self):
        actual_result = ValidatorUtil.validate_uuid4(self._id)

        assert actual_result is True

    def test_validate_uuid4_invalid_uuid(self):
        actual_result = ValidatorUtil.validate_uuid4("848a3cdd")

        assert actual_result is False

    @patch("utils.app_util.AppUtil.get_pyproject_toml_app_version")
    def test_get_app_version_invalid_format(self, mock_get_pyproject_toml_app_version):
        mock_get_pyproject_toml_app_version.return_value = "100"

        with pytest.raises(ValueError) as exc_info:
            AppUtil.get_app_version()

        assert (
            exc_info.value.args[0]
            == "Invalid Application version 100 in pyproject.toml file."
        )

    def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == self._app_version

    @skip
    def test_create_db_url_suffix(self):
        pass

    @skip
    def test_get_alembic_db_url(self):
        pass

    @skip
    def test_get_sqlalchemy_db_url(self):
        pass
