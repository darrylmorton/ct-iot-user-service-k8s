import logging
from typing import Any
from sqlalchemy import select

from . import models, database


# TODO limit and skip
async def get_users():
    session = database.async_session()
    session.begin()

    stmt = select(models.User).limit(25)
    result = await session.execute(stmt)
    await session.close()

    return result.scalars().all()


async def get_user_by_username(username: str):
    session = database.async_session()
    session.begin()

    stmt = select(models.User).where(models.User.username == username)
    result = await session.execute(stmt)
    await session.close()

    return result.scalars().all()


async def post_user(user_request: Any):
    salt = "salt"

    session = database.async_session()
    session.begin()

    user = models.User(
        username=user_request.username,
        password_hash=user_request.password,
        salt=salt,
    )

    session.add(user)
    await session.commit()

    await session.close()

    logging.info(f"*** CRUD post_user {user}")

    return user


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
