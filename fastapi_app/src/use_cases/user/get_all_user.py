from typing import List
from src.schemas.users import User
from src.repositories.user_repository import UserRepository


class GetAllUsersUseCase:
    """Получить всех пользователей"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, skip: int = 0, limit: int = 100, only_active: bool = False) -> List[User]:
        if only_active:
            users = self.repository.get_active_users()
        else:
            users = self.repository.get_all()
        
        return users[skip:skip + limit]