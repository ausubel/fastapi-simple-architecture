from typing import List, Optional
from app.repository.post_repository import PostRepository
from app.repository.models.post_model import PostModel

from app.repository.user_repository import UserRepository
from app.http.exceptions import NotFoundError

class PostService:
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
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

    def delete(self, post_id: int):
        return self.post_repository.delete(post_id)
