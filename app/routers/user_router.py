from fastapi import APIRouter, HTTPException
from app.repository.user_repository import UserRepository
from app.repository.models.user_model import UserModel
from app.services.user_service import UserService
from typing import List
from app.routers.dto.requests.create_user_dto import CreateUserDto
from app.db.dependencies import LocalDb

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_user_service(session: LocalDb) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@user_router.get("/", response_model=List[UserModel])
def get_all_users(session: LocalDb):
    user_service = get_user_service(session)
    return user_service.get_all()

@user_router.post("/")
def create_user(user: CreateUserDto, session: LocalDb):
    user_service = get_user_service(session)
    user_service.create(user.first_name, user.last_name, user.email, user.date_of_birth)
    return {"message": "User created successfully"}

@user_router.get("/{user_id}", response_model=UserModel)
def get_user_by_id(user_id: int, session: LocalDb):
    user_service = get_user_service(session)
    user = user_service.get_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.put("/{user_id}")
def update_user(user_id: int, user: CreateUserDto, session: LocalDb):
    user_service = get_user_service(session)
    user_service.update(user_id, user.first_name, user.last_name, user.email, user.date_of_birth)
    return {"message": "User updated successfully"}

@user_router.delete("/{user_id}")
def delete_user(user_id: int, session: LocalDb):
    user_service = get_user_service(session)
    user_service.delete(user_id)
    return {"message": "User deleted successfully"}
