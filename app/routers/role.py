from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.role import RoleRequest, RoleResponse, AyncRolePermissionRequest, RoleDetailResponse
from app.services import role_service
from app.core.security import require_permission

router = APIRouter(
    tags=["Roles"],
    dependencies=[Depends(require_permission("custom_role_permission"))]
)


@router.get("", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)

@router.get("/{role_id}", response_model=RoleDetailResponse)
def get_roles_by_id(role_id: int,db: Session = Depends(get_db)):
    return role_service.get_roles_by_id(role_id,db)

@router.post("", response_model=RoleResponse)
def create_role( data: RoleRequest, db: Session = Depends(get_db)):
    return role_service.create_role(db, data)

@router.put("/{role_id}", response_model=RoleResponse)
def update_role( role_id: int, data: RoleRequest, db: Session = Depends(get_db)):
    updated = role_service.update_role(db, data, role_id)
    if not updated:
        raise HTTPException(status_code=404, detail="data not found")
    return updated

@router.delete("/{role_id}")
def delete_role(role_id: int,db: Session = Depends(get_db)):
    return role_service.delete_role(db, role_id)

# Permission ass to role
@router.post("/{role_id}/permission")
def assign_permission( data: AyncRolePermissionRequest,role_id:int, db: Session = Depends(get_db)):
    return role_service.assign_permission(db, data, role_id)

