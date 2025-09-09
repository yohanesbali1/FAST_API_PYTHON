from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# custom handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        # ambil pesan error saja
        errors.append(err["msg"])
    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )

async def server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Terjadi kesalahan pada server (500)"},
    )