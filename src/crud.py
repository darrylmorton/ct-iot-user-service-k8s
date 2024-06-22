import uuid
import bcrypt

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import models
import schemas
from database import async_session
from utils import db_util
from logger import log


async def find_users(offset=0) -> list[schemas.User]:
    async with async_session() as session:
        async with session.begin():
            error_message = "Cannot find users"

            try:
                stmt = db_util.find_users_stmt(offset=offset)
                result = await session.execute(stmt)

                return result.scalars().all()
            except SQLAlchemyError:
                log.error(error_message)
                raise SQLAlchemyError(error_message)
            finally:
                await session.close()


async def find_user_by_username(username: str) -> schemas.User:
    async with async_session() as session:
        async with session.begin():
            error_message = f"Cannot find user with username {username=}"

            try:
                stmt = db_util.find_user_by_username_stmt(username=username)
                result = await session.execute(stmt)

                return result.scalars().first()
            except SQLAlchemyError:
                log.error(error_message)
                raise SQLAlchemyError(error_message)
            finally:
                await session.close()


async def add_user(_username: str, _password: str) -> JSONResponse | schemas.User:
    password = _password.encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

    try:
        async with async_session() as session:
            error_message = f"Cannot add user with {_username=}"

            user = db_util.add_user_model(
                username=_username, password_hash=password_hash
            )

            async with session.begin():
                session.add(user)
                await session.commit()

            await session.refresh(user)
            return schemas.User(id=user.id, username=user.username)
    except SQLAlchemyError:
        log.error(error_message)
        raise SQLAlchemyError(error_message)
    finally:
        await session.close()


async def authorise(_username: str, _password: str) -> schemas.UserAuthenticated:
    async with async_session() as session:
        async with session.begin():
            error_message = f"Cannot authorise {_username=}"

            try:
                stmt = db_util.find_user_by_username_stmt(username=_username)
                result = await session.execute(stmt)

                user = result.scalars().first()

                if user:
                    password = _password.encode("utf-8")
                    password_hash = user.password_hash.encode("utf-8")

                    password_match = bcrypt.checkpw(password, password_hash)

                    if password_match:
                        return schemas.UserAuthenticated(
                            id=user.id, username=user.username, enabled=user.enabled
                        )

                return schemas.UserAuthenticated(enabled=False)
            except SQLAlchemyError:
                log.error(error_message)
                raise SQLAlchemyError(error_message)
            finally:
                await session.close()


async def find_user_details(offset=0) -> list[schemas.UserDetails]:
    async with async_session() as session:
        async with session.begin():
            error_message = "Cannot find user details"

            try:
                stmt = db_util.find_user_details_stmt(offset=offset)
                result = await session.execute(stmt)

                return result.scalars().all()
            except SQLAlchemyError:
                log.error(error_message)
                raise SQLAlchemyError(error_message)
            finally:
                await session.close()


async def find_user_details_by_user_id(user_id: uuid, offset=0) -> schemas.UserDetails:
    async with async_session() as session:
        async with session.begin():
            error_message = "Cannot find user details"

            try:
                stmt = db_util.find_user_details_by_user_id_stmt(
                    user_id=user_id, offset=offset
                )
                result = await session.execute(stmt)

                return result.scalars().first()
            except SQLAlchemyError:
                log.error(error_message)
                raise SQLAlchemyError(error_message)
            finally:
                await session.close()


async def add_user_details(
    _user_id: uuid, _first_name: str, _last_name: str
) -> JSONResponse | schemas.UserDetails:
    async with async_session() as session:
        user_details = models.UserDetailsModel(
            user_id=_user_id, first_name=_first_name, last_name=_last_name
        )

        async with session.begin():
            session.add(user_details)
            await session.commit()

        await session.refresh(user_details)
        await session.close()

        return schemas.UserDetails(
            id=user_details.id,
            user_id=user_details.id,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
        )
