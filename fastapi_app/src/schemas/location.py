from pydantic import Field
from datetime import datetime
from src.schemas.base import BaseSchema

class Location(BaseSchema):
    name: str = Field(..., max_length=256)
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)