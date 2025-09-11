from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# custom handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # cek apakah ini JSON invalid
    for err in exc.errors():
        if err.get("type") == "json_invalid":
            return JSONResponse(
                status_code=422,
                content={"errors": "JSON decode error"},
            )

    # kumpulkan semua error
    errors = []
    for err in exc.errors():
        field = next((loc for loc in err["loc"] if loc != "body"), None)
        message = err["msg"]

        if isinstance(field, str):
            error_text = f"{field.capitalize()} {message}"
        else:
            error_text = message

        errors.append(error_text)

    # tampilkan max 1 error, sisanya ringkas jadi "[+X more]"
    max_display = 1
    if len(errors) > max_display:
        shown = errors[0]
        hidden_count = len(errors) - max_display
        error_message = f"{shown} [+{hidden_count} more]"
    else:
        error_message = errors[0] if errors else "Validation error"

    return JSONResponse(
        status_code=422,
        content={"errors": error_message},
    )

# handler untuk HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, "detail": exc.detail},
    )


# handler untuk server error
async def server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Terjadi kesalahan pada server (500)"},
    )
