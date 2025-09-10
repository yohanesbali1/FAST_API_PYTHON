from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from app.routers import auth, user, book , role
from app.helpers.error_handler import validation_exception_handler,server_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="FastAPI JWT")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, server_exception_handler)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
