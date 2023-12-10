import logging
from typing import Any

import bcrypt
from sqlalchemy import select

from . import models, database, config, schemas

LOGGER = logging.getLogger(config.SERVICE_NAME)


# TODO limit and skip
async def find_users() -> list[schemas.User]:
    async with database.async_session() as session:
        async with session.begin():
            stmt = select(models.User).limit(25)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def find_user_by_username(username: str) -> schemas.User:
    async with database.async_session() as session:
        async with session.begin():
            stmt = select(models.User).where(models.User.username == username)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().one()


async def add_user(user_request: Any) -> schemas.User:
    password = user_request.password.encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

    async with database.async_session() as session:
        user = models.User(username=user_request.username, password_hash=password_hash)

        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return schemas.User(id=user.id, username=user.username)


# async def get_user_details(db: AsyncSession):
#     async with database.async_session() as db:
#         async with db.begin():
#             stmt = select(
#                 models.UserDetails.id,
#                 models.UserDetails.user_id,
#                 models.UserDetails.first_name,
#                 models.UserDetails.last_name,
#             )
#
#             result = await db.execute(stmt)
#
#             await db.close()
#
#             return result
