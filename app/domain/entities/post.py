from pydantic import BaseModel
from datetime import datetime

class PostModel(BaseModel):
    id: int
    title: str
    content: str
    userId: int
    created_at: datetime
    updated_at: datetime
