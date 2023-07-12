from typing import Optional

from pydantic import EmailStr, BaseModel


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    is_active: bool = True
    is_superuser: bool = False


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
