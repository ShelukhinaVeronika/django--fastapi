from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema


class User(BaseSchema):
    id: Optional[int] = None
    username: str = Field(..., max_length=150)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    password: str
    is_active: bool = True
    is_superuser: bool = False 
    is_staff: bool = False 
    date_joined: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None


class UserCreate(BaseSchema):
    username: str = Field(..., max_length=150, min_length=3)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    password: str = Field(..., min_length=6)
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    date_joined: datetime = Field(default_factory=datetime.now)


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, max_length=150, min_length=3)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None