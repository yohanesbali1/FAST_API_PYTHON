from app.schemas.response import (
    HTTPErrorResponse,
    ResponseMessage,
    ServerErrorResponse,
    ValidationErrorResponse,
)
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.user import PaginatedUsers, UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.core.security import require_permission


router = APIRouter(
    tags=["Users"],
    dependencies=[
        Depends(
            require_permission("custom_role_permission"),
        )
    ],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code = status.HTTP_201_CREATED,
    description="""
Endpoint untuk membuat pengguna baru.  

- **username**: Nama unik untuk akun  
- **email**: Alamat email yang valid dan belum terdaftar  
- **password**: Password minimal 8 karakter  

Jika berhasil:
- **201 Created** → Mengembalikan data pengguna baru  
Jika gagal:
- **400 Bad Request** → Username atau email sudah digunakan  
- **422 Validation Error** → Input tidak sesuai format  
""",
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    description="""
Endpoint untuk **memperbarui data pengguna** berdasarkan user ID.  

- **user_id**: ID pengguna yang ingin diperbarui (path parameter)  
- **username**: Nama pengguna baru (opsional)  
- **email**: Email baru yang valid (opsional)  
- **password**: Password baru minimal 8 karakter (opsional)  

Jika berhasil:
- **200 OK** → Data pengguna yang diperbarui  
Jika gagal:
- **400 Bad Request** → Data tidak valid atau email sudah digunakan  
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → User dengan ID tersebut tidak ditemukan  
- **422 Validation Error** → Format data tidak sesuai  
""",
)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user, user_id)


@router.get(
    "",
    response_model=PaginatedUsers,
    summary="Get all users",
    description="""
Mengambil daftar pengguna dengan dukungan **pagination**.  

Query parameter:
- **search** (str, optional) → Mencari pengguna berdasarkan username atau email
- **page** (int, default=1) → Halaman yang ingin ditampilkan  
- **per_page** (int, default=10) → Jumlah item per halaman  

Response:
- **200 OK** → Daftar pengguna beserta metadata pagination  
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
""",
)
def list_users(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by username or email"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    return user_service.list_users(db, search, page, per_page)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="""
Endpoint untuk **mengambil data pengguna** berdasarkan ID pengguna.  

- **user_id** (path parameter): ID pengguna yang ingin diambil  

Jika berhasil:
- **200 OK** → Data pengguna  
Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → User dengan ID tersebut tidak ditemukan  
""",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.delete(
    "/{user_id}",
    response_model=ResponseMessage,
    description="""
Endpoint untuk **menghapus pengguna** berdasarkan ID pengguna.  

- **user_id** (path parameter): ID pengguna yang ingin dihapus  

Jika berhasil:
- **200 OK** → Pesan konfirmasi bahwa user berhasil dihapus  
Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → User dengan ID tersebut tidak ditemukan  
""",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)
