from typing import Generator
from my_cookbook.db.session import SessionLocal
from my_cookbook.config import get_settings
from my_cookbook import models, schemas, crud
from fastapi.security import OAuth2PasswordBearer
from my_cookbook.api.v1.core import security
from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

settings = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(current_user: models.User = Depends(get_current_active_user)) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enougg privileges")
    return current_user