from pydantic import BaseModel, SecretStr, Field
from src.schemas.base import BaseSchema

class User(BaseSchema):
    login: str
    password: SecretStr