from pydantic import BaseModel
from typing import Optional

class CreatePostDto(BaseModel):
    title: str
    content: str
    user_id: int
