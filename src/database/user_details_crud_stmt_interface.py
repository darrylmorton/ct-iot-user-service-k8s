import abc
import uuid


class UserDetailsCrudStmtInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_user_details_model(self, user_id: uuid, first_name: str, last_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def find_user_details_by_user_id_stmt(self, user_id: int, offset=0):
        raise NotImplementedError
