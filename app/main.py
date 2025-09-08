from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import auth, user, book , role

app = FastAPI(title="FastAPI JWT")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
