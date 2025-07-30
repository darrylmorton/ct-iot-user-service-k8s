import argparse
import sys
from re import match
from packaging.version import Version, InvalidVersion

sys.path.append("src/")

from logger import log
from utils.app_util import AppUtil


def main(arg_list: list[str] | None = None):
    log.info(f"main called with args: {arg_list}")

    app_version = AppUtil.get_app_version()

    parser = argparse.ArgumentParser(
        description="Check Application version is greater than the Release version."
    )
    parser.add_argument(
        "--release-version", required=True, help="Release version to check"
    )
    args = parser.parse_args(arg_list)

    try:
        release_version = Version(args.release_version)
    except InvalidVersion as e:
        error_message = f"Invalid Release version {args.release_version} does not match semver format: {e}"
        log.error(error_message)

        raise InvalidVersion(error_message)

    if not release_version:
        error_message = f"Invalid Release version {release_version}"
        log.error(error_message)

        raise ValueError(error_message)
    if not match(r"^[0-9]+\.[0-9]+\.[0-9]+$", f"{release_version}"):
        error_message = (
            f"Invalid Release version {release_version} does not match semver format"
        )
        log.error(error_message)

        raise ValueError(error_message)
    if Version(app_version) <= Version(args.release_version):
        error_message = f"Invalid App version {app_version} is less than or equal to the Release version {release_version}"
        log.error(error_message)

        raise ValueError(error_message)

    log.info(
        f"Application version {app_version} is greater than the Release version {args.release_version}."
    )


if __name__ == "__main__":
    main()
