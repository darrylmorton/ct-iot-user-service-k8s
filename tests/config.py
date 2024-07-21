import logging
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = os.environ.get("UVICORN_PORT")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_TOKEN_EXPIRY_SECONDS = int(os.environ.get("JWT_TOKEN_EXPIRY_SECONDS"))

AUTH_SERVICE_HOST = os.environ.get("AUTH_SERVICE_HOST")
AUTH_SERVICE_PORT = os.environ.get("AUTH_SERVICE_PORT")
AUTH_SERVICE_URL = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/api"

DB_USERNAME = os.environ.get("DB_USERNAME") or "postgres"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or "postgres"
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_PORT = os.environ.get("DB_PORT") or 5432
DB_NAME = os.environ.get("DB_NAME") or "users"

DATABASE_URL_PREFIX = "postgresql+asyncpg"
DATABASE_URL_SUFFIX = (
    "{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USERNAME=DB_USERNAME,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_NAME=DB_NAME,
    )
)
DATABASE_URL = f"{DATABASE_URL_PREFIX}://{DATABASE_URL_SUFFIX}"

JWT_EXCLUDED_ENDPOINTS = ["/healthz", "/api/signup"]


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger
