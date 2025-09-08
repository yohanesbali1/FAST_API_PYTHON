from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.user_service import get_user_by_username
from app.utils.hash import verify_password     # ganti ke utils/hash.py
from app.core.security import create_access_token

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def generate_token(user):
    return create_access_token({"sub": user.username})
