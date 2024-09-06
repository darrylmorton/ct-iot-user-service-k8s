import abc


class AdminCrudStmtInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_users_stmt(self, offset=0):
        raise NotImplementedError
