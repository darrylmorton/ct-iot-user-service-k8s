import logging
from fastapi import FastAPI
from src.routers import users, health

from .config import environment, log_level, service_name

logging.basicConfig(level=log_level)
logging.info(F"Environment {environment}")
logging.info(F"Service name {service_name}")
logging.info(F"Log level {log_level}")

app = FastAPI()
app.include_router(health.router)
app.include_router(users.router)
