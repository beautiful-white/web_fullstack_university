from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    guest = "guest"
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.user


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
