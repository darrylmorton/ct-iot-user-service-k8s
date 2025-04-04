import bcrypt

from sqlalchemy.exc import SQLAlchemyError

import schemas
from database.config import async_session
from database.user_crud_interface import UserCrudInterface
from database.user_crud_stmt import UserCrudStmt
from logger import log


class UserCrud(UserCrudInterface):
    def __init__(self):
        super().__init__()
        self.stmt = UserCrudStmt()
        self.session = async_session()

    async def authorise(self, _username: str, _password: str):
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_username_stmt(username=_username)
                    result = await session.execute(stmt)

                    user = result.first()

                    if user:
                        password = _password.encode("utf-8")
                        password_hash = user.password_hash.encode("utf-8")

                        password_match = bcrypt.checkpw(password, password_hash)

                        if password_match:
                            return user

                    return None
                except SQLAlchemyError as error:
                    log.error(f"authorise {error}")
                    raise SQLAlchemyError("Cannot authorise user")
                finally:
                    await session.close()

    async def find_user_by_id(self, _id: str):
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_id_stmt(_id=_id)
                    result = await session.execute(stmt)

                    return result.first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_id {error}")
                    raise SQLAlchemyError("Cannot find user by id")
                finally:
                    await session.close()

    async def find_user_by_username(self, username: str):
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_username_stmt(username=username)
                    result = await session.execute(stmt)

                    return result.first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_username {error}")
                    raise SQLAlchemyError("Cannot find user with username")
                finally:
                    await session.close()

    async def find_user_by_username_and_confirmed(self, username: str):
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_user_by_username_and_confirmed_stmt(
                        username=username
                    )
                    result = await session.execute(stmt)

                    return result.first()
                except SQLAlchemyError as error:
                    log.error(f"find_user_by_username_and_confirmed {error}")
                    raise SQLAlchemyError(
                        "Cannot find user with username and confirmed"
                    )
                finally:
                    await session.close()

    async def add_user(self, _username: str, _password: str):
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
        except Exception as error:
            log.error(f"add_user {error}")
            raise SQLAlchemyError("Cannot add user")
        finally:
            await session.close()

    async def update_confirmed(self, _username: str, _confirmed: bool):
        try:
            async with self.session as session:
                stmt = self.stmt.update_confirmed(
                    _username=_username, _confirmed=_confirmed
                )

                async with session.begin():
                    result = await session.execute(stmt)

                    return result.first()
        except Exception as error:
            log.error(f"update_confirmed {error}")
            raise SQLAlchemyError("Cannot update confirmed")
        finally:
            await session.close()
