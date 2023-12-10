from fastapi import FastAPI

from .routers import healthz, users

server = FastAPI(title="FastAPI server")

server.include_router(healthz.router, include_in_schema=False)
server.include_router(users.router, prefix="/api", tags=["users"])
