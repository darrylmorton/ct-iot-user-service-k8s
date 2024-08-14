import abc
import uuid

from starlette.responses import JSONResponse

import schemas


class AbstractCrud(metaclass=abc.ABCMeta):
    def __init__(self):
        self.session = None

    async def authorise(
        self, _username: str, _password: str
    ) -> schemas.UserAuthenticated:
        pass

    async def find_users(self, offset=0) -> list[schemas.User]:
        pass

    async def find_user_by_id(self, _id: str) -> schemas.User:
        pass

    async def find_user_by_id_and_enabled(self, _id: str) -> schemas.User:
        pass

    async def find_user_by_username(self, username: str) -> schemas.User:
        pass

    async def add_user(
        self, _username: str, _password: str
    ) -> JSONResponse | schemas.User:
        pass

    async def find_user_details(self, offset=0) -> list[schemas.UserDetails]:
        pass

    async def find_user_details_by_user_id(
        self, user_id: uuid, offset=0
    ) -> schemas.UserDetails:
        pass

    async def add_user_details(
        self, _user_id: uuid, _first_name: str, _last_name: str
    ) -> JSONResponse | schemas.UserDetails:
        pass
