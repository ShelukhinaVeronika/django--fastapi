from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.schemas.users import User
from src.schemas.location import Location
from src.schemas.category import Category

class Post(BaseSchema):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    is_published: bool = True
    author: User
    location: Optional[Location] = None 
    category: Optional[Category] = None
    image: Optional[str] = None