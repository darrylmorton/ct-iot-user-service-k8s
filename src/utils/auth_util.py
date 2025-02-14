from http import HTTPStatus

from fastapi import HTTPException

import config
from logger import log
from utils.validator_util import ValidatorUtil


class AuthUtil:
    @staticmethod
    def is_user_valid(_confirmed: bool, _enabled: bool):
        if not _confirmed:
            log.debug("authenticate - user account unconfirmed")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Account unconfirmed"
            )
        if not _enabled:
            log.debug("authenticate - user account suspended")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Account suspended"
            )

    @staticmethod
    def is_admin_valid(_id: str, _is_admin: bool, _admin: bool, _request_path: str):
        if _admin != _is_admin:
            log.debug("authenticate - invalid admin status")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised error"
            )
        if not _admin and _request_path.startswith("/api/admin"):
            log.debug("authenticate - only admins can access admin paths")

            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
            )
        if not _admin:
            for path_prefix in config.UUID_PATH_PARAMS_ROUTES:
                if path_prefix in _request_path:
                    path_params = _request_path.split("/")

                    if len(path_params) != 4:
                        log.debug("authenticate - invalid path")

                        raise HTTPException(
                            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid path"
                        )
                    if not ValidatorUtil.validate_uuid4(path_params[3]):
                        log.debug("authenticate - invalid uuid")

                        raise HTTPException(
                            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id"
                        )
                    if _id != path_params[3]:
                        log.debug(
                            "authenticate - user cannot access another user record"
                        )

                        raise HTTPException(
                            status_code=HTTPStatus.FORBIDDEN, detail="Forbidden error"
                        )
