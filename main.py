from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.user_router import user_router
from app.routers.post_router import post_router
from app.routers.auth_router import auth_router
from app.http.response import ApiResponse
from fastapi.encoders import jsonable_encoder
from app.http.exceptions import AppError

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
    content = jsonable_encoder(ApiResponse(success=False, error="Validation error", code="VALIDATION_ERROR", data=exc.errors()))
    return JSONResponse(status_code=422, content=content)
