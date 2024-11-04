import datetime
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

import config
from logger import log


class TokenUtil:
    @staticmethod
    def create_token_expiry() -> datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=config.JWT_EXPIRY_SECONDS_VERIFY_ACCOUNT
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, config.JWT_SECRET_VERIFY_ACCOUNT, algorithms=["HS256"])

        except TypeError as error:
            log.debug(f"decode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token error"
            )
        except ExpiredSignatureError as error:
            log.debug(f"decode_token - expired signature {error}")

            raise HTTPException(
                status_code=config.HTTP_STATUS_CODE_EXPIRED_TOKEN,
                detail="Expired token error",
            )
        except JWTError as error:
            log.debug(f"decode_token - invalid token {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT"
            )
        except KeyError as error:
            log.debug(f"decode_token - invalid key {error}")

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT payload"
            )

    @staticmethod
    def email_type_selector(_email_type: str) -> str:
        match _email_type:
            case config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE:
                return config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE
            case _:
                log.debug(f"email_type_selector - type not found {_email_type}")

                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Email type not supported"
                )

    @staticmethod
    def encode_token(_username: str, _email_type: str):
        try:
            return {
                "token": jwt.encode(
                    {
                        "username": _username,
                        "email_type": TokenUtil.email_type_selector(_email_type),
                        "exp": TokenUtil.create_token_expiry(),
                    },
                    config.JWT_SECRET_VERIFY_ACCOUNT,
                    algorithm="HS256",
                )
            }
        except KeyError as error:
            log.debug(f"encode_token - key error {error}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token error"
            )
        except TypeError as error:
            log.debug(f"encode_token - type error {error}")

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Token error"
            )
        except JWTError as error:
            log.debug(f"encode_token - jwt error {error}")

            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error
            )
