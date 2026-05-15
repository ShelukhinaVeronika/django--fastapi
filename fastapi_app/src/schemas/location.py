from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.exceptions import ValidationError


class LocationCreate(BaseSchema):
    name: str = Field(..., max_length=256)
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValidationError(
                field="name",
                message="Location name must be at least 2 characters",
                value=v
            )
        if len(v) > 256:
            raise ValidationError(
                field="name",
                message="Location name is too long (max 256 characters)",
                value=v
            )
        return v


class LocationUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None

    @field_validator('name')
    def validate_name(cls, v):
        if v is not None:
            if len(v) < 2:
                raise ValidationError(
                    field="name",
                    message="Location name must be at least 2 characters",
                    value=v
                )
            if len(v) > 256:
                raise ValidationError(
                    field="name",
                    message="Location name is too long (max 256 characters)",
                    value=v
                )
        return v
