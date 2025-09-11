from pydantic import BaseModel, Field
from typing import List


class RoleRequest(BaseModel):
    name: str = Field(..., example="Admin")

class PermissionResponse(BaseModel):
    id: int
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str

class RoleDetailResponse(RoleResponse):
    permissions: List[PermissionResponse] = []
      
class AyncRolePermissionRequest(BaseModel):
    permission_ids: List[int]
    