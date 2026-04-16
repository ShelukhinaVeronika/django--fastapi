from typing import Optional
from src.schemas.users import User
from src.repositories.user_repository import UserRepository


class GetUserByIdUseCase:
    """Получить пользователя по ID"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)