from fastapi import APIRouter, Depends
from typing import List, Annotated
from app.domain.entities.post import PostModel
from app.application.services.post_service import PostService
from app.presentation.dto.create_post_dto import CreatePostDto
from app.presentation.dto.update_post_dto import UpdatePostDto
from app.presentation.response import ApiResponse, ok, created
from app.domain.exceptions import NotFoundError
from app.presentation.dependencies.deps import get_post_service

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

PostServiceDep = Annotated[PostService, Depends(get_post_service)]

@post_router.get("/", response_model=ApiResponse[List[PostModel]])
def get_all_posts(post_service: PostServiceDep):
    data = post_service.get_all()
    return ok(data=data, message="Posts retrieved successfully")

@post_router.post("/", response_model=ApiResponse)
def create_post(post: CreatePostDto, post_service: PostServiceDep):
    post_service.create(post.title, post.content, post.user_id)
    return created(message="Post created successfully")

@post_router.get("/{post_id}", response_model=ApiResponse[PostModel])
def get_post_by_id(post_id: int, post_service: PostServiceDep):
    post = post_service.get_by_id(post_id)
    if post:
        return ok(data=post)
    raise NotFoundError("Post not found", code="POST_NOT_FOUND")

@post_router.put("/{post_id}", response_model=ApiResponse)
def update_post(post_id: int, post: UpdatePostDto, post_service: PostServiceDep):
    post_service.update(post_id, post.title, post.content)
    return ok(message="Post updated successfully")

@post_router.delete("/{post_id}", response_model=ApiResponse)
def delete_post(post_id: int, post_service: PostServiceDep):
    post_service.delete(post_id)
    return ok(message="Post deleted successfully")
