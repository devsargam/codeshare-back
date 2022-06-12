from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    is_admin: Optional[bool] = False


class UserResponseSchema(BaseModel):
    id: int
    username: str
    is_admin: bool
    profile_pic: Optional[str] = None


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
