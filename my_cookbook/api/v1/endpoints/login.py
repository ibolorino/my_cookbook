from typing import Any
from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from my_cookbook import crud
from my_cookbook.config import get_settings
from my_cookbook.api.v1.core import security
from my_cookbook.api.dependencies import get_db

settings = get_settings()

router = APIRouter()


@router.post("/login/")
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password.")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="User is not active.")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
