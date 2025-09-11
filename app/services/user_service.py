from math import ceil
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.hash import hash_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username, email=user.email, password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserUpdate, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="data not found")
    updates = {
        "username": str(user.username).capitalize() if user.username else None,
        "email": user.email,
        "password": hash_password(user.password) if user.password else None,
    }

    for field, value in updates.items():
        if value is not None:
            setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    data = db.query(User).filter(User.username == username).first()
    if not data:
        raise HTTPException(status_code=404, detail="data not found")
    return data


def get_user(db: Session, user_id: int):
    data = db.query(User).filter(User.id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="data not found")
    return UserResponse(**data.__dict__)


def list_users(db: Session, search: Optional[str], page: int, per_page: int):
    query = db.query(User)
    if search:
        query = query.filter(
            User.username.contains(search) | User.email.contains(search)
        )

    total = query.count()
    total_pages = ceil(total / per_page) if total > 0 else 1

    users = query.offset((page - 1) * per_page).limit(per_page).all()

    data = []
    for user in users:
        data.append(UserResponse(id=user.id, username=user.username, email=user.email))

    meta = {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }

    return {"data": data, "meta": meta}


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="data not found")
    db.delete(db_user)
    db.commit()
    return {"status_code": 200, "message": "data deleted"}
