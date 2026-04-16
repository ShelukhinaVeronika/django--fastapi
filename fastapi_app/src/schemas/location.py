from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema


class Location(BaseSchema):
    id: Optional[int] = None
    name: str = Field(..., max_length=256)
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class LocationCreate(BaseSchema):
    name: str = Field(..., max_length=256)
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class LocationUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None