import os

from dotenv import load_dotenv

from utils.app_util import AppUtil

load_dotenv(dotenv_path=".env.test")

SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT") or "local"
ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = os.environ.get("UVICORN_PORT") or 8001
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_TOKEN_EXPIRY_SECONDS = int(os.environ.get("JWT_TOKEN_EXPIRY_SECONDS"))

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
