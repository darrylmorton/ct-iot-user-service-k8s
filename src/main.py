import logging

from fastapi import FastAPI
from src.routers import health, users
from .config import environment, log_level, service_name


logging.basicConfig(level=log_level)
logging.info(f"Environment {environment}")
logging.info(f"Service name {service_name}")
logging.info(f"Log level {log_level}")

app = FastAPI()
app.include_router(health.router)
app.include_router(users.router)
