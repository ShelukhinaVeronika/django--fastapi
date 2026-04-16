from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema


class Post(BaseSchema):
    id: Optional[int] = None
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class PostCreate(BaseSchema):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class PostUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None