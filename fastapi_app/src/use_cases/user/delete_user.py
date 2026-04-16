from src.repositories.user_repository import UserRepository


class DeleteUserUseCase:
    """Удалить пользователя"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int) -> bool:
        return self.repository.delete(user_id)