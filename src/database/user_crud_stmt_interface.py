import abc


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
