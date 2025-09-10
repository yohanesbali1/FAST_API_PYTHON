from pydantic import BaseModel, EmailStr, Field
from typing import List
from app.schemas.role import RoleResponse


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # ✅ ganti orm_mode


class MetaData(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginatedUsers(BaseModel):
    data: List[UserResponse]
    meta: MetaData


class ShowUser(UserResponse):
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True  # ✅ ganti orm_mode
