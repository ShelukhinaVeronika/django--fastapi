from pydantic import Field
from datetime import datetime
from src.schemas.base import BaseSchema

class Category(BaseSchema):
    title: str = Field(..., max_length=256)
    description: str
    slug: str = Field(..., pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.now)