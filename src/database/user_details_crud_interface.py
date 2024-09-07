import abc
import uuid

from starlette.responses import JSONResponse

import schemas


class UserDetailsCrudInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.session = None

    @abc.abstractmethod
    async def add_user_details(
        self, _user_id: uuid, _first_name: str, _last_name: str
    ) -> JSONResponse | schemas.UserDetails:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_user_details_by_user_id(
        self, user_id: uuid, offset=0
    ) -> schemas.UserDetails:
        raise NotImplementedError
