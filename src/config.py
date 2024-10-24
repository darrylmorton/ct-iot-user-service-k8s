import os

from dotenv import load_dotenv

from utils.app_util import AppUtil


load_dotenv()

APP_VERSION = AppUtil.get_app_version()

AWS_REGION = os.environ.get("AWS_REGION")
SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT") or "local"
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8001

AUTH_SERVICE_ENDPOINT = os.environ.get("AUTH_SERVICE_URL")
AUTH_SERVICE_URL = f"{AUTH_SERVICE_ENDPOINT}/api"

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL_PREFIX = "postgresql+asyncpg"
DATABASE_URL_SUFFIX = AppUtil.create_db_url_suffix(DB_PASSWORD)
DATABASE_URL = f"{DATABASE_URL_PREFIX}://{DATABASE_URL_SUFFIX}"

JWT_EXCLUDED_ENDPOINTS = [
    "/openapi.json",
    "/docs",
    "/healthz",
    "/api/signup",
    "/api/login",
    "/favicon.ico",
]

UUID_PATH_PARAMS_ROUTES = ["/api/users/", "/api/user-details/"]
