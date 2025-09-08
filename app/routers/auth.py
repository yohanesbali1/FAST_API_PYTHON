from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services import auth_service
from app.services.user_service import create_user, get_user_by_username
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.username, payload.password)
    token = auth_service.generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # cek apakah username/email sudah ada
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # simpan user baru
    new_user = create_user(db, user)
    return new_user