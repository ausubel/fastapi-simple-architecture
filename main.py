from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.presentation.api.user_router import user_router
from app.presentation.api.post_router import post_router
from app.presentation.api.auth_router import auth_router
from app.presentation.response import ApiResponse
from app.domain.exceptions import AppError

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)

@app.exception_handler(AppError)
async def app_error_handler(_, exc: AppError):
    content = jsonable_encoder(ApiResponse(success=False, error=exc.message, code=exc.code))
    return JSONResponse(status_code=exc.status_code, content=content)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(_, exc: RequestValidationError):
    errors = exc.errors()
    for error in errors:
        error.pop("ctx", None)
        error.pop("url", None)
    content = jsonable_encoder(ApiResponse(success=False, error="Validation error", code="VALIDATION_ERROR", data=errors))
    return JSONResponse(status_code=422, content=content)
