from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    error: str | None = None
    code: str | None = None

def ok(data: Any | None = None, message: str | None = None):
    content = jsonable_encoder(ApiResponse[T](success=True, data=data, message=message))
    return JSONResponse(status_code=200, content=content)

def created(data: Any | None = None, message: str | None = None):
    content = jsonable_encoder(ApiResponse[T](success=True, data=data, message=message))
    return JSONResponse(status_code=201, content=content)

def custom(status_code: int, data: Any | None = None, message: str | None = None, code: str | None = None):
    content = jsonable_encoder(ApiResponse[T](success=True, data=data, message=message, code=code))
    return JSONResponse(status_code=status_code, content=content)

def no_content():
    return Response(status_code=204)
