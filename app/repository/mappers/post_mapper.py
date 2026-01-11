from app.repository.models.post_model import PostModel

class PostMapper:
    @staticmethod
    def to_model(row: tuple) -> PostModel:
        # Assuming query returns: id, title, content, userId, createdAt, updatedAt
        return PostModel(
            id=row[0],
            title=row[1],
            content=row[2],
            userId=row[3],
            created_at=row[4],
            updated_at=row[5]
        )
