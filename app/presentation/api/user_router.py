from fastapi import APIRouter, Depends
from typing import List, Annotated
from app.domain.entities.user import UserModel
from app.application.services.user_service import UserService
from app.application.services.auth_service import AuthService
from app.presentation.dto.create_user_dto import CreateUserDto
from app.presentation.dto.update_user_dto import UpdateUserDto
from app.presentation.response import ApiResponse, ok, created
from app.domain.exceptions import NotFoundError
from app.presentation.dependencies.deps import get_current_user, get_current_admin, get_user_service, get_auth_service

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

@user_router.get("/", response_model=ApiResponse[List[UserModel]], dependencies=[Depends(get_current_admin)])
def get_all_users(user_service: UserServiceDep):
    data = user_service.get_all()
    return ok(data=data, message="Users retrieved successfully")

@user_router.post("/", response_model=ApiResponse[UserModel], include_in_schema=False, dependencies=[Depends(get_current_admin)])
def create_user(user: CreateUserDto, user_service: UserServiceDep, auth_service: AuthServiceDep):
    hashed_password = auth_service.get_password_hash(user.password)
    user_service.create(user.first_name, user.last_name, user.email, hashed_password, user.date_of_birth)
    return created(message="User created successfully")

@user_router.get("/{user_id}", response_model=ApiResponse[UserModel], dependencies=[Depends(get_current_user)])
def get_user_by_id(user_id: int, user_service: UserServiceDep):
    user = user_service.get_by_id(user_id)
    if user:
        return ok(data=user)
    raise NotFoundError("User not found", code="USER_NOT_FOUND")

@user_router.put("/{user_id}", response_model=ApiResponse[UserModel], dependencies=[Depends(get_current_user)])
def update_user(user_id: int, user: UpdateUserDto, user_service: UserServiceDep):
    user_service.update(user_id, user.first_name, user.last_name, user.email, user.date_of_birth)
    return ok(message="User updated successfully")

@user_router.delete("/{user_id}", response_model=ApiResponse, dependencies=[Depends(get_current_admin)])
def delete_user(user_id: int, user_service: UserServiceDep):
    user_service.delete(user_id)
    return ok(message="User deleted successfully")
