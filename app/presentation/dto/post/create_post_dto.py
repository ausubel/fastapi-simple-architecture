from pydantic import BaseModel, Field

class CreatePostDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the post")
    content: str = Field(..., min_length=1, description="Content of the post")
    user_id: int = Field(..., description="ID of the author")
