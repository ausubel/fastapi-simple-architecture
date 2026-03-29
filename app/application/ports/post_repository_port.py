from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.post import PostModel

class PostRepositoryPort(ABC):
    @abstractmethod
    def get_all(self) -> List[PostModel]:
        pass

    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional[PostModel]:
        pass

    @abstractmethod
    def create(self, title: str, content: str, user_id: int):
        pass

    @abstractmethod
    def update(self, post_id: int, title: str, content: str):
        pass

    @abstractmethod
    def delete(self, post_id: int):
        pass
