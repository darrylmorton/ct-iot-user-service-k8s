import os
from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get("ENVIRONMENT")
log_level = os.environ.get("LOG_LEVEL")
service_name = os.environ.get("SERVICE_NAME")

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
