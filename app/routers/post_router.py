from fastapi import APIRouter
from typing import List
from app.repository.post_repository import PostRepository
from app.repository.user_repository import UserRepository
from app.repository.models.post_model import PostModel
from app.services.post_service import PostService
from app.routers.dto.requests.create_post_dto import CreatePostDto
from app.db.dependencies import LocalDb
from app.http.response import ApiResponse, ok, created
from app.http.exceptions import NotFoundError

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


def get_post_service(session: LocalDb) -> PostService:
    post_repository = PostRepository(session)
    user_repository = UserRepository(session)
    return PostService(post_repository, user_repository)

@post_router.get("/", response_model=ApiResponse[List[PostModel]])
def get_all_posts(session: LocalDb):
    post_service = get_post_service(session)
    data = post_service.get_all()
    return ok(data=data, message="Posts retrieved successfully")

@post_router.post("/", response_model=ApiResponse)
def create_post(post: CreatePostDto, session: LocalDb):
    post_service = get_post_service(session)
    post_service.create(post.title, post.content, post.user_id)
    return created(message="Post created successfully")

@post_router.get("/{post_id}", response_model=ApiResponse[PostModel])
def get_post_by_id(post_id: int, session: LocalDb):
    post_service = get_post_service(session)
    post = post_service.get_by_id(post_id)
    if post:
        return ok(data=post)
    raise NotFoundError("Post not found", code="POST_NOT_FOUND")

@post_router.delete("/{post_id}", response_model=ApiResponse)
def delete_post(post_id: int, session: LocalDb):
    post_service = get_post_service(session)
    post_service.delete(post_id)
    return ok(message="Post deleted successfully")
