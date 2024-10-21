from http import HTTPStatus
from uuid import UUID

from anyio import value
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from logger import log
from utils.app_util import AppUtil


class UserBase(BaseModel):
    id: UUID
    username: str


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserAuthenticated(UserBase):
    username: str = Field(None, exclude=True)

    enabled: bool
    is_admin: bool

    class ConfigDict:
        from_attributes = True


class UserRequest(UserBase):
    id: UUID = Field(None, exclude=True)
    password: str


class UserDetailsBase(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        if (
            info.field_name == "first_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="1 Invalid first_name"
            )

        return v

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        if (
            info.field_name == "last_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="1 Invalid last_name"
            )

        return v


class UserDetails(UserDetailsBase):
    class ConfigDict:
        from_attributes = True


class UserDetailsRequest(UserDetailsBase):
    id: UUID = Field(None, exclude=True)


class SignupBase(BaseModel):
    id: str
    user_id: str
    username: str
    password: str
    first_name: str
    last_name: str

    # @field_validator("id")
    # @classmethod
    # def validate_id(cls, v: str, info: ValidationInfo):
    #     if info.field_name == "id" and not isinstance(v, str):
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id"
    #         )
    #
    #     return v
    #
    # @field_validator("user_id")
    # @classmethod
    # def validate_user_id(cls, v: str, info: ValidationInfo):
    #     if info.field_name == "user_id" and not isinstance(v, str):
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST, detail="Invalid user id"
    #         )
    #
    #     return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        if info.field_name == "username" and not AppUtil.validate_email(v):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invalid username or password",
            )

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        if (
            info.field_name == "password"
            and not isinstance(v, str)
            or len(v) < 8
            or len(v) > 16
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invalid username or password",
            )

        return v

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        if info.field_name == "first_name":
            log.info(f"{v=}")

        if (
            info.field_name == "first_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="2 Invalid first_name"
            )

        return v

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        if info.field_name == "last_name":
            log.info(f"{v=}")

        if (
            info.field_name == "last_name"
            and not isinstance(v, str)
            or len(v) < 2
            or len(v) > 30
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="2 Invalid last_name"
            )

        return v


class SignupRequest(SignupBase):
    id: str = Field(None, exclude=True)
    user_id: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class SignupResponse(SignupBase):
    id: str = Field(None, exclude=True)
    user_id: str = Field(None, exclude=True)
    password: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class LoginBase(BaseModel):
    id: UUID
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        if info.field_name == "username" and not AppUtil.validate_email(v):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid login"
            )

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        if (
            info.field_name == "password"
            and not isinstance(v, str)
            or len(v) < 8
            or len(v) > 16
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid login"
            )

        return v


class LoginRequest(LoginBase):
    id: UUID = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True
