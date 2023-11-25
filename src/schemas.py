from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int
    username: str


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserRequest(UserBase):
    id: int = Field(None, exclude=True)
    password: str


class UserDetailsBase(BaseModel):
    id: int
    user_id: int


class UserDetails(UserDetailsBase):
    first_name: str
    last_name: str

    class ConfigDict:
        from_attributes = True
