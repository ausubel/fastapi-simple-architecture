from pydantic import BaseModel, Field

class UpdatePostDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the post")
    content: str = Field(..., min_length=1, description="Content of the post")
