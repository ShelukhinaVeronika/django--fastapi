from pydantic import Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.exceptions import ValidationError


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

    @field_validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValidationError(
                field="username",
                message="Username must contain only letters and numbers",
                value=v
            )
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValidationError(
                field="password",
                message="Password must be at least 6 characters",
                value=v
            )
        return v
    
    @field_validator('first_name')
    def validate_first_name(cls, v):
        if v is not None and len(v) < 2:
            raise ValidationError(
                field="first_name",
                message="First name must be at least 2 characters",
                value=v
            )
        return v
    
    @field_validator('last_name')
    def validate_last_name(cls, v):
        if v is not None and len(v) < 2:
            raise ValidationError(
                field="last_name",
                message="Last name must be at least 2 characters",
                value=v
            )
        return v


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, max_length=150, min_length=3)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None

    @field_validator('username')
    def validate_username(cls, v):
        if v is not None and not v.isalnum():
            raise ValidationError(
                field="username",
                message="Username must contain only letters and numbers",
                value=v
            )
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 6:
                raise ValidationError(
                    field="password",
                    message="Password must be at least 6 characters",
                    value=v
                )
        return v
    
    @field_validator('first_name')
    def validate_first_name(cls, v):
        if v is not None and len(v) < 2:
            raise ValidationError(
                field="first_name",
                message="First name must be at least 2 characters",
                value=v
            )
        return v
    
    @field_validator('last_name')
    def validate_last_name(cls, v):
        if v is not None and len(v) < 2:
            raise ValidationError(
                field="last_name",
                message="Last name must be at least 2 characters",
                value=v
            )
        return v
