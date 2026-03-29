from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserService
from app.presentation.response import ApiResponse, created
from app.presentation.dto.register_user_dto import RegisterUserDto
from app.presentation.dto.login_dto import LoginDto
from app.presentation.dependencies.deps import get_user_service, get_auth_service

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

class TokenDto(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/register", response_model=ApiResponse)
def register(user: RegisterUserDto, user_service: UserServiceDep, auth_service: AuthServiceDep):
    hashed_password = auth_service.get_password_hash(user.password)
    user_service.create(user.first_name, user.last_name, user.email, hashed_password, user.date_of_birth)
    return created(message="User registered successfully")

@auth_router.post("/login", response_model=ApiResponse[TokenDto])
def login(login_data: LoginDto, user_service: UserServiceDep, auth_service: AuthServiceDep):
    user = user_service.get_by_email(login_data.email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not auth_service.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": user.email, "role_id": user.role_id, "user_id": user.id})
    
    return ApiResponse(
        success=True,
        data=TokenDto(access_token=access_token, token_type="bearer"),
        message="Login successful"
    )

@auth_router.post("/token", response_model=TokenDto, include_in_schema=False)
def login_for_docs(user_service: UserServiceDep, auth_service: AuthServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    # Swagger sends username, but we use email
    user = user_service.get_by_email(form_data.username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not auth_service.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": user.email, "role_id": user.role_id, "user_id": user.id})
    
    return TokenDto(access_token=access_token, token_type="bearer")
