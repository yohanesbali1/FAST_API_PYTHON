from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from app.core.config import settings
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_username
from datetime import datetime, timedelta



def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.JWT_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

bearer_scheme = HTTPBearer()  

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if not user:
        raise credentials_exception
    permissions = set()
    for role in user.roles:  
     
        for perm in getattr(role, "permissions", []):
            permissions.add(perm.name)
    setattr(user, "permissions", list(permissions))

    return user

def require_permission(permission: str):
    def permission_checker(current_user = Depends(get_current_user)):
        if permission not in getattr(current_user, "permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tidak memiliki akses"
            )
        return current_user
    return permission_checker