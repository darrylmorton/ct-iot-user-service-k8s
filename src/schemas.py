from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str


class User(UserBase):
    class ConfigDict:
        from_attributes = True


class UserDetailsBase(BaseModel):
    id: int
    user_id: int


class UserDetails(UserDetailsBase):
    first_name: str
    last_name: str

    class ConfigDict:
        from_attributes = True
