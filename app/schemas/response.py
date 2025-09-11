from pydantic import BaseModel
from typing import List


class ValidationErrorResponse(BaseModel):
    errors: List[str]


class HTTPErrorResponse(BaseModel):
    status_code: int
    detail: str


class ServerErrorResponse(BaseModel):
    error: str

class ResponseMessage(BaseModel):
    status_code: int
    message: str