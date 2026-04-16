# src/schemas/category.py
from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema


class Category(BaseSchema):
    id: Optional[int] = None
    title: str = Field(..., max_length=256)
    description: str
    slug: str = Field(..., pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class CategoryCreate(BaseSchema):
    title: str = Field(..., max_length=256)
    description: str
    slug: str = Field(..., pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class CategoryUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(None, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: Optional[bool] = None