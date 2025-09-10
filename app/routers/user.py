from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.core.security import require_permission

router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(require_permission("custom_role_permission"))]
)

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.patch("/{user_id}")
def update_user(user_id: int, user:UserCreate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user, user_id)

@router.get("")
def list_users(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by username or email"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    
):
    return user_service.list_users(db,search,page,per_page)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)