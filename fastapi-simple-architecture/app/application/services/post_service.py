from typing import List, Optional
from app.application.ports.post_repository_port import PostRepositoryPort
from app.domain.entities.post import PostModel
from app.application.ports.user_repository_port import UserRepositoryPort
from app.domain.exceptions import NotFoundError

class PostService:
    def __init__(self, post_repository: PostRepositoryPort, user_repository: UserRepositoryPort):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def get_all(self) -> List[PostModel]:
        return self.post_repository.get_all()

    def get_by_id(self, post_id: int) -> Optional[PostModel]:
        return self.post_repository.get_by_id(post_id)

    def create(self, title: str, content: str, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found", code="USER_NOT_FOUND")
        return self.post_repository.create(title, content, user_id)

    def update(self, post_id: int, title: str, content: str):
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post not found", code="POST_NOT_FOUND")
        return self.post_repository.update(post_id, title, content)

    def delete(self, post_id: int):
        return self.post_repository.delete(post_id)
