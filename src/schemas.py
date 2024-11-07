from http import HTTPStatus
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from utils.validator_util import ValidatorUtil


class UserBase(BaseModel):
    id: UUID
    username: str


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserAuthenticated(BaseModel):
    id: str
    confirmed: bool
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
        return ValidatorUtil.validate_id(v, info)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_user_id(v, info)

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


class SignupRequest(SignupBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "foo@example.com",
                    "password": "barbarba",
                    "first_name": "Foo",
                    "last_name": "Bar",
                }
            ]
        }
    }

    id: str = Field(None, exclude=True)
    user_id: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class LoginBase(BaseModel):
    id: str
    username: str
    password: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str, info: ValidationInfo):
        return ValidatorUtil.validate_id(v, info)

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


class LoginRequest(LoginBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "foo@example.com",
                    "password": "barbarba",
                }
            ]
        }
    }

    id: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True
