from pathlib import Path
from re import match
from urllib.parse import quote

import toml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import config


class AppUtil:
    @staticmethod
    def set_openapi_info(app: FastAPI) -> FastAPI:
        app.openapi_schema = get_openapi(
            title=config.SERVICE_NAME,
            version=AppUtil.get_app_version(),
            routes=app.routes,
        )

        return app

    @staticmethod
    def get_pyproject_toml_app_version():
        file_path = Path(__file__).parent.parent.parent / "pyproject.toml"

        if file_path.exists() and file_path.is_file():
            return toml.load(file_path)["tool"]["poetry"]["version"]

        raise FileNotFoundError(
            f"pyproject.toml file not found at {file_path}. Please ensure it exists in the project root directory."
        )

    @staticmethod
    def get_app_version():
        app_version = AppUtil.get_pyproject_toml_app_version()

        if not match("^[0-9]+\.[0-9]+\.[0-9]+$", app_version):
            raise ValueError(
                f"Invalid Application version {app_version} in pyproject.toml file."
            )

        return app_version

    @staticmethod
    def create_db_url_suffix(password=config.DB_PASSWORD) -> str:
        return "{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
            DB_USERNAME=config.DB_USERNAME,
            DB_PASSWORD=password,
            DB_HOST=config.DB_HOST,
            DB_PORT=config.DB_PORT,
            DB_NAME=config.DB_NAME,
        )

    @staticmethod
    def get_alembic_db_url() -> str:
        db_password = quote(config.DB_PASSWORD).replace("%", "%%")

        return f"postgresql://{AppUtil.create_db_url_suffix(db_password)}"

    @staticmethod
    def get_sqlalchemy_db_url() -> str:
        return f"postgresql+asyncpg://{AppUtil.create_db_url_suffix()}"

    @staticmethod
    def is_excluded_endpoint(request_path: str) -> bool:
        for item in config.JWT_EXCLUDED_ENDPOINTS:
            if item == request_path:
                return True

        return False
