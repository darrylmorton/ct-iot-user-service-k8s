import abc
from uuid import UUID

from sqlalchemy.sql.dml import ReturningUpdate


class UserCrudStmtInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_user_model(self, username: str, password_hash: str):
        raise NotImplementedError

    @abc.abstractmethod
    def find_user_by_id_stmt(self, _id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def find_user_by_username_stmt(self, username: str):
        raise NotImplementedError

    @abc.abstractmethod
    def find_user_by_username_and_confirmed_stmt(self, username: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_confirmed(
        self, _username: str, _confirmed: bool
    ) -> ReturningUpdate[tuple[UUID, str, bool]]:
        raise NotImplementedError
