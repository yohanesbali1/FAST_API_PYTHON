from math import ceil
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.hash import hash_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username, email=user.email, password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserCreate, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="data not found")
    db_user.username = user.username
    db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session, search: Optional[str], page: int, per_page: int):
    query = db.query(User)
    if search:
        query = query.filter(
            User.username.contains(search) | User.email.contains(search)
        )

    # Meta pagination
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
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
