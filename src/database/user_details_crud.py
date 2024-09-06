import uuid

from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

import schemas
from database.config import async_session
from database.user_details_crud_interface import UserDetailsCrudInterface
from database.user_details_crud_stmt import UserDetailsCrudStmt
from logger import log


class UserDetailsCrud(UserDetailsCrudInterface):
    def __init__(self):
        super().__init__()
        self.stmt = UserDetailsCrudStmt()
        self.session = async_session()

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
