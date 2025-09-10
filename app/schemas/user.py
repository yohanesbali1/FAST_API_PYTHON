from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.role import RoleResponse





class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # ✅ ganti orm_mode
class ShowUser(UserResponse):
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True  # ✅ ganti orm_mode