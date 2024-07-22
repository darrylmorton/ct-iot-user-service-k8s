from pathlib import Path

import toml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import config


def set_openapi_info(app: FastAPI) -> FastAPI:
    app.openapi_schema = get_openapi(
        title=config.SERVICE_NAME,
        version=config.APP_VERSION,
        routes=app.routes,
    )

    return app


def get_app_version():
    app_version = None

    pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"

    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        app_version = toml.load(pyproject_toml_file)["tool"]["poetry"]["version"]

    return app_version
