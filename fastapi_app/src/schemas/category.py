from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.exceptions import ValidationError

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

    @field_validator('title')
    def validate_title(cls, v):
        if len(v) < 3:
            raise ValidationError(
                field="title",
                message="Title must be at least 3 characters",
                value=v
            )
        return v
    
    @field_validator('slug')
    def validate_slug(cls, v):
        if len(v) < 3:
            raise ValidationError(
                field="slug",
                message="Slug must be at least 3 characters",
                value=v
            )
        return v


class CategoryUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(None, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: Optional[bool] = None

    @field_validator('title')
    def validate_title(cls, v):
        if v is not None and len(v) < 3:
            raise ValidationError(
                field="title",
                message="Title must be at least 3 characters",
                value=v
            )
        return v
    
    @field_validator('slug')
    def validate_slug(cls, v):
        if v is not None and len(v) < 3:
            raise ValidationError(
                field="slug",
                message="Slug must be at least 3 characters",
                value=v
            )
        return v
