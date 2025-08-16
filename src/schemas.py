from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.types import UuidVersion

from utils.validator_util import ValidatorUtil


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: UUID = Annotated[UUID, UuidVersion(4)]
    username: str


class UserAuthenticated(User):
    id: UUID = Annotated[UUID, UuidVersion(4)]
    confirmed: bool
    enabled: bool
    is_admin: bool


class UserDetailsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserDetails(UserDetailsBase):
    id: UUID = Annotated[UUID, UuidVersion(4)]
    user_id: UUID = Annotated[UUID, UuidVersion(4)]
    first_name: str
    last_name: str

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: str):
        return ValidatorUtil.validate_id(str(v))

    @field_validator("user_id", mode="before")
    @classmethod
    def validate_user_id(cls, v: str):
        return ValidatorUtil.validate_user_id(str(v))

    @field_validator("first_name", mode="before")
    @classmethod
    def validate_first_name(cls, v: str):
        return ValidatorUtil.validate_first_name(v)

    @field_validator("last_name", mode="before")
    @classmethod
    def validate_last_name(cls, v: str):
        return ValidatorUtil.validate_last_name(v)


class UserDetailsRequest(UserDetailsBase):
    id: UUID = Annotated[UUID, UuidVersion(4)]


class SignupBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "foo@example.com",
                    "password": "barbarba",
                    "first_name": "Foo",
                    "last_name": "Bar",
                }
            ]
        },
    )


class SignupRequest(SignupBase):
    username: str
    password: str
    first_name: str
    last_name: str

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, v: str):
        return ValidatorUtil.validate_username(
            v, HTTPStatus.BAD_REQUEST, "/signup", "Invalid username"
        )

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str):
        return ValidatorUtil.validate_password(
            v, HTTPStatus.BAD_REQUEST, "/signup", "Invalid password"
        )

    @field_validator("first_name", mode="before")
    @classmethod
    def validate_first_name(cls, v: str):
        return ValidatorUtil.validate_first_name(v)

    @field_validator("last_name", mode="before")
    @classmethod
    def validate_last_name(cls, v: str):
        return ValidatorUtil.validate_last_name(v)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "foo@example.com",
                    "password": "barbarba",
                    "first_name": "Foo",
                    "last_name": "Bar",
                }
            ]
        },
    )


class LoginBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "foo@example.com",
                    "password": "barbarba",
                }
            ]
        },
    )


class LoginRequest(LoginBase):
    username: str
    password: str

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, v: str):
        return ValidatorUtil.validate_username(
            v, HTTPStatus.UNAUTHORIZED, "/login", "Invalid login"
        )

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str):
        return ValidatorUtil.validate_password(
            v, HTTPStatus.UNAUTHORIZED, "/login", "Invalid login"
        )
