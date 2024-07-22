from pathlib import Path

import toml


def get_app_version():
    app_version = None

    pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"

    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        app_version = toml.load(pyproject_toml_file)["tool"]["poetry"]["version"]

    return app_version
