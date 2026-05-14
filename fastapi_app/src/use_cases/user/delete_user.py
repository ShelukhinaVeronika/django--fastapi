from src.repositories.user_repository import UserRepository
from src.exceptions import NotFoundError


class DeleteUserUseCase:
    """Удалить пользователя"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int) -> bool:
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)
        
        return self.repository.delete(user_id)
