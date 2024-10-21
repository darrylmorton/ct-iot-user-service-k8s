from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
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
    id: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class JwtAuthTokenBase(BaseModel):
    auth_token: str = Field(alias="auth-token", validation_alias="auth_token")


class JwtAuthToken(JwtAuthTokenBase):
    @field_validator("auth_token")
    @classmethod
    def validate_auth_token_header(cls, v: str, info: ValidationInfo):
        if info.field_name == "auth_token" and not isinstance(v, str):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid request header"
            )

        # try:
        #     payload = AuthUtil.decode_token(v)
        #
        #     JwtPayload.model_validate(payload)
        # except KeyError:
        #     raise HTTPException(
        #         status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid JWT payload"
        #     )

        return v

    class ConfigDict:
        from_attributes = True