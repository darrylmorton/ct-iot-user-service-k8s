from http import HTTPStatus

from pydantic import BaseModel, Field, field_validator, ConfigDict, UUID4
from pydantic_core.core_schema import ValidationInfo

from utils.validator_util import ValidatorUtil


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: UUID4
    username: str


class UserAuthenticated(User):
    id: str
    confirmed: bool
    enabled: bool
    is_admin: bool


class UserDetailsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserDetails(UserDetailsBase):
    id: UUID4
    user_id: UUID4
    first_name: str
    last_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_id(str(v), info)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_user_id(str(v), info)

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_first_name(v, info)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_last_name(v, info)


class UserDetailsRequest(UserDetailsBase):
    id: str = Field(None, exclude=True)


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

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_username(
            v, info, HTTPStatus.BAD_REQUEST, "Invalid username or password"
        )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_password(
            v, info, HTTPStatus.BAD_REQUEST, "Invalid username or password"
        )

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_first_name(v, info)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_last_name(v, info)

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

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_username(
            v, info, HTTPStatus.UNAUTHORIZED, "Invalid login"
        )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_password(
            v, info, HTTPStatus.UNAUTHORIZED, "Invalid login"
        )
