from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from my_cookbook import crud
from my_cookbook.api.dependencies import get_db
from my_cookbook.config import get_settings
from my_cookbook.models.user import UserCreate, UserRead

settings = get_settings()


router = APIRouter(prefix="/user")


@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)) -> Any:
    users = crud.user.get_multi(db=db)
    return users


@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Username already in use.")
    user = crud.user.create(db, obj_in=user_in)
    return user
