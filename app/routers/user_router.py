from fastapi import APIRouter, Depends
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.repository.models.user_model import UserModel
from app.services.user_service import UserService
from typing import List
from app.routers.dto.requests.create_user_dto import CreateUserDto
from app.db.dependencies import LocalDb
from app.http.response import ApiResponse, ok, created
from app.http.exceptions import NotFoundError
from app.routers.deps import get_current_user, get_current_admin

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_user_service(session: LocalDb) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@user_router.get("/", response_model=ApiResponse[List[UserModel]], dependencies=[Depends(get_current_admin)])
def get_all_users(session: LocalDb):
    user_service = get_user_service(session)
    data = user_service.get_all()
    return ok(data=data, message="Users retrieved successfully")

@user_router.post("/", response_model=ApiResponse[UserModel], include_in_schema = False, dependencies=[Depends(get_current_admin)])
def create_user(user: CreateUserDto, session: LocalDb):
    user_service = get_user_service(session)
    auth_service = AuthService()
    hashed_password = auth_service.get_password_hash(user.password)
    user_service.create(user.first_name, user.last_name, user.email, hashed_password, user.date_of_birth)
    return created(message="User created successfully")

@user_router.get("/{user_id}", response_model=ApiResponse[UserModel], dependencies=[Depends(get_current_user)])
def get_user_by_id(user_id: int, session: LocalDb):
    user_service = get_user_service(session)
    user = user_service.get_by_id(user_id)
    if user:
        return ok(data=user)
    raise NotFoundError("User not found", code="USER_NOT_FOUND")

@user_router.put("/{user_id}", response_model=ApiResponse[UserModel], dependencies=[Depends(get_current_user)])
def update_user(user_id: int, user: CreateUserDto, session: LocalDb):
    user_service = get_user_service(session)
    user_service.update(user_id, user.first_name, user.last_name, user.email, user.date_of_birth)
    return ok(message="User updated successfully")

@user_router.delete("/{user_id}", response_model=ApiResponse, dependencies=[Depends(get_current_admin)])
def delete_user(user_id: int, session: LocalDb):
    user_service = get_user_service(session)
    user_service.delete(user_id)
    return ok(message="User deleted successfully")
