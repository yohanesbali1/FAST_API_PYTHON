from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.schemas.response import (
    ValidationErrorResponse,
    HTTPErrorResponse,
    ServerErrorResponse,
)


def custom_openapi(app: FastAPI):
    def _custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description="Project sederhana dengan JWT Authentication dan Custom Global Error Responses untuk memastikan keamanan, konsistensi, serta dokumentasi API yang jelas.",
            routes=app.routes,
        )

        RESPONSES = {
            401: {
                "content": {"application/json": {"schema": HTTPErrorResponse.schema()}},
                "description": "Unauthorized error",
            },
            403: {
                "content": {"application/json": {"schema": HTTPErrorResponse.schema()}},
                "description": "Forbidden error",
            },
            404: {
                "content": {"application/json": {"schema": HTTPErrorResponse.schema()}},
                "description": "Not found error",
            },
            422: {
                "content": {
                    "application/json": {"schema": ValidationErrorResponse.schema()}
                },
                "description": "Validasi gagal",
            },
            500: {
                "content": {
                    "application/json": {"schema": ServerErrorResponse.schema()}
                },
                "description": "Server error",
            },
        }
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["responses"].update(
                    {str(k): v for k, v in RESPONSES.items()}
                )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = _custom_openapi
