from http import HTTPStatus

from starlette.responses import JSONResponse

from logger import log
from schemas import UserAuthenticated, User
# from utils.app_util import AppUtil


class AuthUtil:
    pass
    # @staticmethod
    # def is_user_valid(
    #     _user: User | UserAuthenticated, _status_code: int
    # ) -> JSONResponse | bool:
    #     return (
    #         AuthUtil.user_exists(_user, _status_code)
    #         and AuthUtil.is_user_confirmed(_user, _status_code)
    #         and AuthUtil.is_user_enabled(_user, _status_code)
    #     )
    #
    # @staticmethod
    # def user_exists(user: UserAuthenticated, status_code: int):
    #     if not user:
    #         log.debug("authenticate - user not found")
    #
    #         return JSONResponse(status_code=status_code, content="Unauthorised error")
    #
    #     return True
    #
    # @staticmethod
    # def is_user_confirmed(
    #     _user: UserAuthenticated, status_code: int
    # ) -> JSONResponse | bool:
    #     log.debug(f"{_user=}")
    #
    #     if not _user.confirmed:
    #         log.debug("Login - account unconfirmed")
    #
    #         return JSONResponse(status_code=status_code, content="Account unconfirmed")
    #
    #     return True
    #
    # @staticmethod
    # def is_user_enabled(
    #     _user: UserAuthenticated, status_code: int
    # ) -> JSONResponse | bool:
    #     if not _user.enabled:
    #         log.debug("Login - account not enabled")
    #
    #         return JSONResponse(status_code=status_code, content="Account not enabled")
    #
    #     return True
    #
    # @staticmethod
    # def is_admin_valid(
    #     _admin: bool, _user: User, _request_path: str
    # ) -> JSONResponse | bool:
    #     return AuthUtil.is_admin_status_valid(_admin=_admin, _user=_user)
    #
    # @staticmethod
    # def is_admin_status_valid(_admin: bool, _user: User) -> JSONResponse | bool:
    #     if _admin != _user.is_admin:
    #         log.debug("authenticate - invalid admin status")
    #
    #         return JSONResponse(
    #             status_code=HTTPStatus.UNAUTHORIZED, content="Unauthorised error"
    #         )
    #
    #     return True
    #
    # @staticmethod
    # def is_admin_access_valid(
    #     _admin: bool, _user: User, _request_path: str
    # ) -> JSONResponse | bool:
    #     if not _user.is_admin and _request_path.startswith("/api/admin"):
    #         log.debug("authenticate - only admins can access admin paths")
    #
    #         return JSONResponse(
    #             status_code=HTTPStatus.FORBIDDEN, content="Forbidden error"
    #         )
    #
    #     return True
    #
    # @staticmethod
    # def is_user_access_valid(
    #     _user: UserAuthenticated, _request_path: str
    # ) -> JSONResponse | bool:
    #     if not _user.is_admin and not AppUtil.validate_uuid_path_param(
    #         _request_path, str(_user.id)
    #     ):
    #         log.debug("authenticate - user cannot access another user record")
    #
    #         return JSONResponse(
    #             status_code=HTTPStatus.FORBIDDEN, content="Forbidden error"
    #         )
    #
    #     return True
