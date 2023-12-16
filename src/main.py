from fastapi import FastAPI

from .routers import healthz, auth, users

server = FastAPI(title="FastAPI server")

server.include_router(healthz.router, include_in_schema=False)

# TODO authenticated access required except for signup
#  middleware and/or config required via FastAPI?
server.include_router(auth.router, prefix="/api", tags=["auth"])
server.include_router(users.router, prefix="/api", tags=["users"])
