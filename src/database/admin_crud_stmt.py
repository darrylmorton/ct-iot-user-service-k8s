from sqlalchemy import select

from database import models
from database.admin_crud_stmt_interface import AdminCrudStmtInterface


class AdminCrudStmt(AdminCrudStmtInterface):
    def find_users_stmt(self, offset=0):
        return (
            select(models.UserModel.id, models.UserModel.username)
            .limit(25)
            .offset(offset)
        )
