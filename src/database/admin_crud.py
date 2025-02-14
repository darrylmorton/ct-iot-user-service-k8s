from sqlalchemy.exc import SQLAlchemyError

from database.admin_crud_interface import AdminCrudInterface
from database.config import async_session
from database.admin_crud_stmt import AdminCrudStmt
from logger import log


class AdminCrud(AdminCrudInterface):
    def __init__(self):
        super().__init__()
        self.stmt = AdminCrudStmt()
        self.session = async_session()

    async def find_users(self, offset=0):
        async with self.session as session:
            async with session.begin():
                try:
                    stmt = self.stmt.find_users_stmt(offset=offset)
                    result = await session.execute(stmt)

                    return result.all()
                except SQLAlchemyError as error:
                    log.error(f"find_users {error}")
                    raise SQLAlchemyError("Cannot find users")
                finally:
                    await session.close()
