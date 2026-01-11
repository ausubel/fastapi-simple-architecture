from typing import List, Optional
from app.db.dependencies import LocalDb
from app.repository.models.post_model import PostModel
from app.repository.mappers.post_mapper import PostMapper

class PostRepository:
    def __init__(self, session: LocalDb):
        self.session = session

    def get_all(self) -> List[PostModel]:
        rows = self.session.fetch_all("SELECT id, title, content, userId, createdAt, updatedAt FROM posts")
        return [PostMapper.to_model(row) for row in rows]

    def get_by_id(self, post_id: int) -> Optional[PostModel]:
        row = self.session.fetch_one(
            "SELECT id, title, content, userId, createdAt, updatedAt FROM posts WHERE id = ?",
            (post_id,)
        )
        if row:
            return PostMapper.to_model(row)
        return None

    def create(self, title: str, content: str, user_id: int):
        self.session.execute(
            "INSERT INTO posts (title, content, userId) VALUES (?, ?, ?)",
            (title, content, user_id),
        )

    def delete(self, post_id: int):
        self.session.execute("DELETE FROM posts WHERE id = ?", (post_id,))
