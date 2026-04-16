from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema


class Comment(BaseSchema):
    id: Optional[int] = None
    text: str = Field(..., min_length=1)
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    is_published: bool = True


class CommentCreate(BaseSchema):
    text: str = Field(..., min_length=1)
    post_id: int
    author_id: int
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class CommentUpdate(BaseSchema):
    text: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None