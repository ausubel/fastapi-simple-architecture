from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.db.dependencies import LocalDb
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.http.response import ApiResponse, created
from app.routers.dto.requests.register_user_dto import RegisterUserDto
from app.routers.dto.requests.login_dto import LoginDto

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

class TokenDto(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/register", response_model=ApiResponse)
def register(user: RegisterUserDto, session: LocalDb):

    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    
    auth_service = AuthService()

    hashed_password = auth_service.get_password_hash(user.password)
    
    user_service.create(user.first_name, user.last_name, 
    user.email, hashed_password, user.date_of_birth)
    
    return created(message="User registered successfully")

@auth_router.post("/login", response_model=ApiResponse[TokenDto])
def login(login_data: LoginDto, session: LocalDb):
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    
    user = user_service.get_by_email(login_data.email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    auth_service = AuthService()
    
    if not auth_service.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": user.email, "role_id": user.role_id, "user_id": user.id})
    
    return ApiResponse(
        success=True,
        data=TokenDto(access_token=access_token, token_type="bearer"),
        message="Login successful"
    )

