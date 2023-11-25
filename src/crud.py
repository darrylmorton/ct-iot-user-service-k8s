import logging
from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from . import models


# TODO limit and skip
async def get_users(db: AsyncSession):
    return await db.execute(select(models.User.id, models.User.username).limit(25))


async def get_user_by_username(db: AsyncSession, username: str):
    return await db.execute(select(
        models.User.id, models.User.username
    ).where(username=username).limit(1))


async def post_user(db: AsyncSession, user_request: Any):
    logging.info(f"*** post_user user_request {user_request}")
    salt = "salt"
    user = User(username=user_request.username, password_hash=user_request.password, salt=salt)

    db.add(user)
    await db.commit()


async def get_user_details(db: AsyncSession):
    return await db.execute(
        select(
            models.UserDetails.id,
            models.UserDetails.user_id,
            models.UserDetails.first_name,
            models.UserDetails.last_name,
        )
    )
