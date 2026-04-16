from src.schemas.users import User, UserCreate
from src.repositories.user_repository import UserRepository


class CreateUserUseCase:
    """Создать нового пользователя"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_data: UserCreate) -> User:
        if not user_data.password or len(user_data.password) < 6:
            raise ValueError("Password is required and must be at least 6 characters")
        
        existing_email = self.repository.get_by_email(user_data.email)
        if existing_email:
            raise ValueError(f"User with email '{user_data.email}' already exists")
        
        existing_username = self.repository.get_by_username(user_data.username)
        if existing_username:
            raise ValueError(f"User with username '{user_data.username}' already exists")
        
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=user_data.password,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
            is_staff=user_data.is_staff,
            date_joined=user_data.date_joined,
            last_login=None
        )
        
        return self.repository.create(new_user)