from pydantic import Field
from datetime import datetime
from src.schemas.base import BaseSchema
from src.schemas.users import User

class Comment(BaseSchema):
    text: str
    author: User
    created_at: datetime = Field(default_factory=datetime.now)
    is_published: bool = True