from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    id: UUID
    username: EmailStr


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserAuthenticated(UserBase):
    is_admin: bool
    enabled: bool

    class ConfigDict:
        from_attributes = True


class UserRequest(UserBase):
    id: UUID = Field(None, exclude=True)
    password: str = Field(min_length=8, max_length=16)


class UserDetailsBase(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)


class UserDetails(UserDetailsBase):
    class ConfigDict:
        from_attributes = True


class UserDetailsRequest(UserDetailsBase):
    id: UUID = Field(None, exclude=True)


class SignupBase(BaseModel):
    id: UUID
    user_id: UUID
    username: EmailStr
    password: str = Field(min_length=8, max_length=16)
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)


class SignupRequest(SignupBase):
    id: UUID = Field(None, exclude=True)
    user_id: UUID = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class SignupResponse(SignupBase):
    id: UUID = Field(None, exclude=True)
    user_id: UUID = Field(None, exclude=True)
    password: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class LoginBase(BaseModel):
    id: UUID
    username: EmailStr
    password: str = Field(min_length=8, max_length=16)


class LoginRequest(LoginBase):
    id: UUID = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True
