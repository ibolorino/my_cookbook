import uuid
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    full_name: Optional[str]
    email: Optional[EmailStr] = Field(unique=True)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class User(UserBase, table=True):
    __tablename__ = "users"
    hashed_password: Optional[str]


class UserRead(UserBase):
    pass


class UserCreate(SQLModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str


class UserUpdate(SQLModel):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True
