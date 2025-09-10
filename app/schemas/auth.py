from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
