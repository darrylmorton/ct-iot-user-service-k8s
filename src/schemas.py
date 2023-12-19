from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    id: int
    username: EmailStr


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserAuthenticated(UserBase):
    enabled: bool

    class ConfigDict:
        from_attributes = True


class UserRequest(UserBase):
    id: int = Field(None, exclude=True)
    password: str = Field(min_length=8, max_length=16)


class UserDetailsBase(BaseModel):
    id: int
    user_id: int
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)


class UserDetails(UserDetailsBase):
    class ConfigDict:
        from_attributes = True


class UserDetailsRequest(UserDetailsBase):
    id: int = Field(None, exclude=True)


class SignupBase(BaseModel):
    id: int
    user_id: int
    username: EmailStr
    password: str = Field(min_length=8, max_length=16)
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)


class SignupRequest(SignupBase):
    id: int = Field(None, exclude=True)
    user_id: int = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class SignupResponse(SignupBase):
    id: int = Field(None, exclude=True)
    user_id: int = Field(None, exclude=True)
    password: str = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True


class LoginBase(BaseModel):
    id: int
    username: EmailStr
    password: str = Field(min_length=8, max_length=16)


class LoginRequest(LoginBase):
    id: int = Field(None, exclude=True)

    class ConfigDict:
        from_attributes = True

