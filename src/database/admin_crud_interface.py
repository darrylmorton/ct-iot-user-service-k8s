import abc

import schemas


class AdminCrudInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.session = None

    @abc.abstractmethod
    async def find_users(self, offset=0) -> list[schemas.User]:
        raise NotImplementedError
