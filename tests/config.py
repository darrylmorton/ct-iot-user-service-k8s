import os

from dotenv import load_dotenv

from utils.app_util import AppUtil

load_dotenv(dotenv_path=".test.env")

AWS_REGION = os.environ.get("AWS_REGION")
# SES_SOURCE = os.environ.get("SES_SOURCE")
USERNAME = os.environ.get("USERNAME")

SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT") or "local"
ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = os.environ.get("UVICORN_PORT") or 8002
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS"))

QUEUE_PROTOCOL = os.environ.get("QUEUE_PROTOCOL")
QUEUE_HOST = os.environ.get("QUEUE_HOST")
QUEUE_PORTS = os.environ.get("QUEUE_PORTS")
QUEUE_ACKS = os.environ.get("QUEUE_ACKS")
QUEUE_POLL_WAIT_SECONDS = int(os.environ.get("QUEUE_POLL_WAIT_SECONDS"))
QUEUE_TOPIC_NAME = os.environ.get("QUEUE_TOPIC_NAME")
QUEUE_GROUP_ID = os.environ.get("QUEUE_GROUP_ID")
EMAIL_ACCOUNT_VERIFICATION_TYPE = "ACCOUNT_VERIFICATION"

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

HTTP_STATUS_CODE_EXPIRED_TOKEN = 498
JWT_SECRET_VERIFY_ACCOUNT = os.environ.get("JWT_SECRET_VERIFY_ACCOUNT")
JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT = int(
    os.environ.get("JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT")
)
ALB_URL = os.environ.get("ALB_URL")
