from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_cookbook import crud, schemas
from my_cookbook.api.dependencies import get_db
from my_cookbook.config import get_settings

settings = get_settings()


router = APIRouter(prefix="/user")


@router.get("/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Username already in use.")
    user = crud.user.create(db, obj_in=user_in)
    return user
