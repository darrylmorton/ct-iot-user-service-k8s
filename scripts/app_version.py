from re import match

from logger import log
from utils.app_util import AppUtil


def get_app_version():
    app_version = AppUtil.get_pyproject_toml_app_version()

    if not match("^[0-9]+\.[0-9]+\.[0-9]+$", app_version):
        log.error(f"Invalid Application version {app_version} in pyproject.toml file.")

        raise ValueError(
            f"Invalid Application version {app_version} in pyproject.toml file."
        )

    log.info(f"Application version {app_version} in pyproject.toml file.")

    return app_version


if __name__ == "__main__":
    get_app_version()
