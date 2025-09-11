from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.role import Role, Permission
from app.schemas.role import RoleRequest


def create_role(db: Session, data: RoleRequest):
    db_data = Role(name=data.name)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_roles(db: Session):
    return db.query(Role).all()


def update_role(db: Session, data: RoleRequest, role_id: int):
    db_data = db.query(Role).filter(Role.id == role_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Role not found")
    db_data.name = data.name
    db.commit()
    db.refresh(db_data)
    return db_data


def get_roles_by_id(role_id: int, db: Session):
    return db.query(Role).filter(Role.id == role_id).first()


def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.users = []
    role.permissions = []

    db.delete(role)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "message": f"Role '{role.name}' deleted successfully",
    }


def assign_permission(db: Session, data, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Cek apakah permission ada
    permissions = (
        db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
    )
    if len(permissions) != len(data.permission_ids):
        raise HTTPException(status_code=404, detail="Permissions not found")

    # Hapus semua permission lama, ganti dengan baru
    role.permissions = permissions

    db.commit()
    db.refresh(role)
    return {
        "status_code": status.HTTP_200_OK,
        "message": f"Role '{role.name}' updated successfully",
    }
