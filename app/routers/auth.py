from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services import auth_service
from app.services.user_service import create_user, get_user_by_username
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_current_user

router = APIRouter(
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    description="""
Login endpoint dengan menggunakan username dan password.  

- **username**: Nama pengguna yang terdaftar  
- **password**: Password sesuai dengan akun  

Jika berhasil, API akan mengembalikan:
- **200 OK** → JWT access token
- **401 Unauthorized** → Username atau password salah
- **422 Validation Error** → Input tidak sesuai format
""",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.username, payload.password)
    token = auth_service.generate_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/profile",
    response_model=UserResponse,
    description="""
Endpoint untuk mendapatkan data profil pengguna yang sedang login.  

- Endpoint ini memerlukan **Authorization Header** dengan format:  
  `Authorization: Bearer <access_token>`  

Jika berhasil:
- **200 OK** → Data profil pengguna  
Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
""",
)
def get_profile(current_user=Depends(get_current_user)):
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    description="""
Endpoint untuk registrasi pengguna baru.  

- **username**: Nama unik untuk akun baru  
- **email**: Email yang valid dan belum digunakan  
- **password**: Password minimal 8 karakter  

Jika berhasil:
- **201 Created** → Data pengguna baru  
Jika gagal:
- **400 Bad Request** → Username atau email sudah terdaftar  
- **422 Validation Error** → Format data tidak sesuai  
""",
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = create_user(db, user)
    return new_user
