from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.exceptions import ValidationError


class Comment(BaseSchema):
    id: Optional[int] = None
    text: str = Field(..., min_length=1)
    image: Optional[str] = None
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    is_published: bool = True


class CommentCreate(BaseSchema):
    text: str = Field(..., min_length=1)
    image: Optional[str] = None
    post_id: int
    author_id: Optional[int] = None
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("text")
    def validate_text(cls, v):
        if len(v) < 1:
            raise ValidationError(
                field="text", message="Comment text cannot be empty", value=v
            )
        if len(v) > 1000:
            raise ValidationError(
                field="text",
                message="Comment text is too long (max 1000 characters)",
                value=v,
            )
        return v

    @field_validator("post_id")
    def validate_post_id(cls, v):
        if v <= 0:
            raise ValidationError(
                field="post_id", message="post_id must be a positive integer", value=v
            )
        return v

    @field_validator("author_id")
    def validate_author_id(cls, v):
        if v <= 0:
            raise ValidationError(
                field="author_id",
                message="author_id must be a positive integer",
                value=v,
            )
        return v


class CommentUpdate(BaseSchema):
    text: Optional[str] = Field(None, min_length=1)
    image: Optional[str] = None
    is_published: Optional[bool] = None

    @field_validator("text")
    def validate_text(cls, v):
        if v is not None:
            if len(v) < 1:
                raise ValidationError(
                    field="text", message="Comment text cannot be empty", value=v
                )
            if len(v) > 1000:
                raise ValidationError(
                    field="text",
                    message="Comment text is too long (max 1000 characters)",
                    value=v,
                )
        return v
