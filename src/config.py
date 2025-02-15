import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.environ.get("AWS_REGION")
# SES_SOURCE = os.environ.get("SES_SOURCE")

SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT") or "local"
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE"))
SENTRY_SAMPLE_RATE = int(os.environ.get("SENTRY_SAMPLE_RATE"))

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOG_LEVEL = os.environ.get("LOG_LEVEL")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
APP_PORT = os.environ.get("UVICORN_PORT") or 8002

QUEUE_PROTOCOL = os.environ.get("QUEUE_PROTOCOL")
QUEUE_HOST = os.environ.get("QUEUE_HOST")
QUEUE_PORTS = os.environ.get("QUEUE_PORTS")
QUEUE_ACKS = os.environ.get("QUEUE_ACKS")
QUEUE_POLL_WAIT_SECONDS = int(os.environ.get("QUEUE_POLL_WAIT_SECONDS"))
QUEUE_TOPIC_NAME = os.environ.get("QUEUE_TOPIC_NAME")
QUEUE_GROUP_ID = os.environ.get("QUEUE_GROUP_ID")
EMAIL_ACCOUNT_VERIFICATION_TYPE = os.environ.get("EMAIL_ACCOUNT_VERIFICATION_TYPE")

AUTH_SERVICE_ENDPOINT = os.environ.get("AUTH_SERVICE_URL")
AUTH_SERVICE_URL = f"{AUTH_SERVICE_ENDPOINT}/api"

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

HTTP_STATUS_CODE_EXPIRED_TOKEN = 498
JWT_SECRET_VERIFY_ACCOUNT = os.environ.get("JWT_SECRET_VERIFY_ACCOUNT")
JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT = int(
    os.environ.get("JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT")
)
ALB_URL = os.environ.get("ALB_URL")

JWT_EXCLUDED_ENDPOINTS = [
    "/favicon.ico",
    "/openapi.json",
    "/docs",
    "/healthz",
    "/api/signup",
    "/api/login",
    "/api/verify-account/",
    "/metrics",
    "/metrics/",
]

UUID_PATH_PARAMS_ROUTES = ["/api/users/", "/api/user-details/"]
