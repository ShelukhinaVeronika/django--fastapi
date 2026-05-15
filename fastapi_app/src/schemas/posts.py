from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.exceptions import ValidationError


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
    
    @field_validator('author_id')
    def validate_author_id(cls, v):
        if v <= 0:
            raise ValidationError(
                field="author_id",
                message="author_id must be a positive integer",
                value=v
            )
        return v
    
    @field_validator('category_id')
    def validate_category_id(cls, v):
        if v is not None and v <= 0:
            raise ValidationError(
                field="category_id",
                message="category_id must be a positive integer",
                value=v
            )
        return v
    
    @field_validator('location_id')
    def validate_location_id(cls, v):
        if v is not None and v <= 0:
            raise ValidationError(
                field="location_id",
                message="location_id must be a positive integer",
                value=v
            )
        return v


class PostUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None
    
    
    @field_validator('category_id')
    def validate_category_id(cls, v):
        if v is not None and v <= 0:
            raise ValidationError(
                field="category_id",
                message="category_id must be a positive integer",
                value=v
            )
        return v
    
    @field_validator('location_id')
    def validate_location_id(cls, v):
        if v is not None and v <= 0:
            raise ValidationError(
                field="location_id",
                message="location_id must be a positive integer",
                value=v
            )
        return v