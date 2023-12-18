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


class UserDetails(UserDetailsBase):
    first_name: str
    last_name: str

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
