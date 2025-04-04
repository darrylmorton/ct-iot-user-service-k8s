import abc


class AdminCrudInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.session = None

    @abc.abstractmethod
    async def find_users(self, offset=0):
        raise NotImplementedError
