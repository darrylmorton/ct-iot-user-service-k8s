from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from utils.app_util import AppUtil


def validate_id(v: str, info: ValidationInfo):
    if info.field_name == "id" and not AppUtil.validate_uuid4(v):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid id")

    return v


def validate_user_id(v: str, info: ValidationInfo):
    if info.field_name == "user_id" and not AppUtil.validate_uuid4(v):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid user id"
        )

    return v


def validate_username(v: str, info: ValidationInfo, status_code, message: str):
    if info.field_name == "username" and not AppUtil.validate_email(v):
        raise HTTPException(
            status_code=status_code,
            detail=message,
        )

    return v


def validate_password(v: str, info: ValidationInfo, status_code, message: str):
    if (
        info.field_name == "password"
        and not isinstance(v, str)
        or len(v) < 8
        or len(v) > 16
    ):
        raise HTTPException(
            status_code=status_code,
            detail=message,
        )

    return v


def validate_first_name(v: str, info: ValidationInfo):
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


def validate_last_name(v: str, info: ValidationInfo):
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
    id: str = Field(None, exclude=True)
    password: str


class UserDetailsBase(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        return validate_id(str(v), info)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str, info: ValidationInfo):
        return validate_user_id(str(v), info)

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        return validate_first_name(v, info)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        return validate_last_name(v, info)


class UserDetails(UserDetailsBase):
    class ConfigDict:
        from_attributes = True


class UserDetailsRequest(UserDetailsBase):
    id: str = Field(None, exclude=True)


class SignupBase(BaseModel):
    id: str
    user_id: str
    username: str
    password: str
    first_name: str
    last_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        return validate_id(v, info)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str, info: ValidationInfo):
        return validate_user_id(v, info)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        return validate_username(
            v, info, HTTPStatus.BAD_REQUEST, "Invalid username or password"
        )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        return validate_password(
            v, info, HTTPStatus.BAD_REQUEST, "Invalid username or password"
        )

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        return validate_first_name(v, info)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        return validate_last_name(v, info)


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
    id: str
    username: str
    password: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        return validate_id(v, info)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        return validate_username(v, info, HTTPStatus.UNAUTHORIZED, "Invalid login")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        return validate_password(v, info, HTTPStatus.UNAUTHORIZED, "Invalid login")


class LoginRequest(LoginBase):
    id: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True
