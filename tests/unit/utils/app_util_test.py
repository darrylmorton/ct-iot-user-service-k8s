from unittest import skip
from unittest.mock import patch

import pytest

from utils.app_util import AppUtil
from utils.validator_util import ValidatorUtil


class TestAppUtil:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    _app_version = "2.0.1"

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

    @skip(
        reason="This test needs to be moved to the check_version.py script tests <= asserts"
    )
    @patch("utils.app_util.AppUtil.get_pyproject_toml_app_version")
    def test_get_app_version_matches_release(self, mock_get_pyproject_toml_app_version):
        mock_get_pyproject_toml_app_version.return_value = self._app_version

        with pytest.raises(ValueError) as exc_info:
            AppUtil.get_app_version()

        assert (
            exc_info.value.args[0]
            == "Invalid Application version 100 in pyproject.toml file."
        )

    # @patch("utils.app_util.toml.load")
    # def test_get_app_version_less_than_release(self, mocked_toml_load):
    #     mocked_toml_load.return_value = "1.9.9"
    #     # mock toml file import to return an invalid version format
    #     # actual_result = AppUtil.get_app_version()
    #
    #     with pytest.raises(ValueError):
    #         AppUtil.get_app_version()

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
