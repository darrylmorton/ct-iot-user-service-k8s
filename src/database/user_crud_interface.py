import abc
import uuid

from sqlalchemy.sql.dml import ReturningUpdate
from starlette.responses import JSONResponse

import schemas


class UserCrudInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.session = None

    @abc.abstractmethod
    async def add_user(
        self, _username: str, _password: str
    ) -> JSONResponse | schemas.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def authorise(self, _username: str, _password: str) -> schemas.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_user_by_id(self, _id: uuid) -> schemas.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_user_by_username(self, username: str) -> schemas.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_user_by_username_and_confirmed(self, username: str) -> schemas.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_confirmed(
        self, _username: str, _confirmed: bool
    ) -> ReturningUpdate[tuple[uuid.UUID, str, bool]]:
        raise NotImplementedError
