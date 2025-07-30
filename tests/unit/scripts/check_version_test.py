import pytest
from packaging.version import InvalidVersion

from scripts.__main__ import main


class TestCheckVersionScript:
    _app_version = "2.0.1"

    def test_get_app_version_matches_release(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--release-version", self._app_version])

        assert (
            exc_info.value.args[0]
            == "Invalid App version 2.0.1 is less than or equal to the Release version 2.0.1"
        )

    def test_get_app_version_less_than_release(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--release-version", "2.0.2"])

        assert (
            exc_info.value.args[0]
            == "Invalid App version 2.0.1 is less than or equal to the Release version 2.0.2"
        )

    def test_release_version_invalid_semver_number(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--release-version", "2"])

        assert (
            exc_info.value.args[0]
            == "Invalid Release version 2 does not match semver format"
        )

    def test_release_version_invalid_semver_letter(self):
        with pytest.raises(InvalidVersion) as exc_info:
            main(["--release-version", "a"])

        assert (
            exc_info.value.args[0]
            == "Invalid Release version a does not match semver format: Invalid version: 'a'"
        )

    def test_get_app_version_greater_than_release(self):
        main(["--release-version", "2.0.0"])
