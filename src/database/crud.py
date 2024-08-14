import uuid

import bcrypt

from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import schemas
from database.abstract_crud import AbstractCrud
from database.crud_stmt import CrudStmt
from database.config import async_session
from logger import log


class Crud(AbstractCrud):
    def __init__(self):
        super().__init__()
        self.stmt = CrudStmt()
        self.session = async_session()

    async def authorise(
        self, _username: str, _password: str
    ) -> schemas.UserAuthenticated:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_username_stmt(username=_username)
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
                except SQLAlchemyError as error:
                    log.error(f"authorise {error}")
                    raise SQLAlchemyError("Cannot authorise user")
                finally:
                    await session.close()

    async def find_users(self, offset=0) -> list[schemas.User]:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_users_stmt(offset=offset)
                    result = await session.execute(stmt)

                    return result.scalars().all()
                except SQLAlchemyError as error:
                    log.error(f"find_users {error}")
                    raise SQLAlchemyError("Cannot find users")
                finally:
                    await session.close()

    async def find_user_by_id(self, _id: str) -> schemas.User:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_id_stmt(_id=_id)
                    result = await session.execute(stmt)

                    return result.scalars().first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_id {error}")
                    raise SQLAlchemyError("Cannot find user by id")
                finally:
                    await session.close()

    async def find_user_by_id_and_enabled(self, _id: str) -> schemas.User:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_id_and_enabled_stmt(_id=_id)
                    result = await session.execute(stmt)

                    return result.scalars().first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_id_and_enabled {error}")
                    raise SQLAlchemyError("Cannot find enabled user by id")
                finally:
                    await session.close()

    async def find_user_by_username(self, username: str) -> schemas.User:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_username_stmt(username=username)
                    result = await session.execute(stmt)

                    return result.scalars().first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_username {error}")
                    raise SQLAlchemyError("Cannot find user with username")
                finally:
                    await session.close()

    async def add_user(
        self, _username: str, _password: str
    ) -> JSONResponse | schemas.User:
        password = _password.encode("utf-8")

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

        try:
            async with self.session as session:
                user = self.stmt.add_user_model(
                    username=_username, password_hash=password_hash
                )

                async with session.begin():
                    session.add(user)
                    await session.commit()

                await session.refresh(user)
                return schemas.User(id=user.id, username=user.username)
        except SQLAlchemyError as error:
            log.error(f"add_user {error}")
            raise SQLAlchemyError("Cannot add user")
        finally:
            await session.close()

    async def find_user_details(self, offset=0) -> list[schemas.UserDetails]:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_details_stmt(offset=offset)
                    result = await session.execute(stmt)

                    return result.scalars().all()
                except SQLAlchemyError as error:
                    log.error(f"find_user_details {error}")
                    raise SQLAlchemyError("Cannot find user details")
                finally:
                    await session.close()

    async def find_user_details_by_user_id(
        self, user_id: uuid, offset=0
    ) -> schemas.UserDetails:
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_details_by_user_id_stmt(
                        user_id=user_id, offset=offset
                    )
                    result = await session.execute(stmt)

                    return result.scalars().first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_details_by_user_id {error}")
                    raise SQLAlchemyError("Cannot find user details")
                finally:
                    await session.close()

    async def add_user_details(
        self, _user_id: uuid, _first_name: str, _last_name: str
    ) -> JSONResponse | schemas.UserDetails:
        try:
            async with self.session as session:
                user_details = self.stmt.add_user_details_model(
                    user_id=_user_id, first_name=_first_name, last_name=_last_name
                )

                async with session.begin():
                    session.add(user_details)
                    await session.commit()

                await session.refresh(user_details)

                return schemas.UserDetails(
                    id=user_details.id,
                    user_id=user_details.user_id,
                    first_name=user_details.first_name,
                    last_name=user_details.last_name,
                )
        except SQLAlchemyError as error:
            log.error(f"add_user_details {error}")
            raise SQLAlchemyError("Cannot add user details")
        finally:
            await session.close()
