from app.schemas.response import ResponseMessage
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.role import (
    RoleRequest,
    RoleResponse,
    AyncRolePermissionRequest,
    RoleDetailResponse,
)
from app.services import role_service
from app.core.security import require_permission

router = APIRouter(
    tags=["Roles"], dependencies=[Depends(require_permission("custom_role_permission"))]
)


@router.get(
    "",
    response_model=list[RoleResponse],
    summary="Get all roles",
    description="""
Endpoint untuk mengambil data role.  

Jika berhasil:
- **200 OK** → Mengembalikan data role (atau daftar role)  

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa 
""",
)
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleDetailResponse,
    status_code=status.HTTP_200_OK,
    description="""
Endpoint untuk mengambil data role berdasarkan ID role.  

- **role_id**: ID role yang ingin diambil  

Jika berhasil:
- **200 OK** → Mengembalikan data role  

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → Role dengan ID tersebut tidak ditemukan  
""",
)
def get_roles_by_id(role_id: int, db: Session = Depends(get_db)):
    return role_service.get_roles_by_id(role_id, db)


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    description="""
Endpoint untuk membuat role baru.

- **name**: Nama unik untuk role

Jika berhasil:
- **201 Created** → Mengembalikan data role baru yang dibuat

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa
- **422 Validation Error** → Input tidak sesuai format yang diharapkan
""",
)
def create_role(data: RoleRequest, db: Session = Depends(get_db)):
    return role_service.create_role(db, data)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    description="""
Endpoint untuk memperbarui role.

- **role_id**: ID role yang ingin diperbarui (path parameter)
- **name**: Nama unik untuk role

Jika berhasil:
- **200 OK** → Mengembalikan data role yang diperbarui

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa
- **404 Not Found** → Role dengan ID tersebut tidak ditemukan
- **422 Validation Error** → Input tidak sesuai format yang diharapkan
""",
)
def update_role(role_id: int, data: RoleRequest, db: Session = Depends(get_db)):
    return role_service.update_role(db, data, role_id)


@router.delete(
    "/{role_id}",
    response_model=ResponseMessage,
    status_code=status.HTTP_200_OK,
    description="""
Endpoint untuk menghapus role.

- **role_id**: ID role yang ingin dihapus (path parameter)

Jika berhasil:
- **200 OK** → Mengembalikan data role yang dihapus

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa
- **404 Not Found** → Role dengan ID tersebut tidak ditemukan
""",
)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return role_service.delete_role(db, role_id)


@router.post(
    "/{role_id}/permission",
    response_model=ResponseMessage,
    status_code=status.HTTP_200_OK,
    description="""
Endpoint untuk memperbarui role dengan permission.

- **role_id**: ID role yang ingin diperbarui (path parameter)
- **permission_ids**: ID permission yang ingin diperbarui (path parameter)

Jika berhasil:
- **200 OK** → Mengembalikan data role yang diperbarui

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa
- **404 Not Found** → Role dengan ID tersebut tidak ditemukan
- **422 Validation Error** → Input tidak sesuai format yang diharapkan
""",
)
def assign_permission(
    data: AyncRolePermissionRequest, role_id: int, db: Session = Depends(get_db)
):
    return role_service.assign_permission(db, data, role_id)
