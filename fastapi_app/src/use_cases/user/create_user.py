from src.schemas.users import User, UserCreate
from src.repositories.user_repository import UserRepository
from src.exceptions import UniqueConstraintError, ValidationError


class CreateUserUseCase:
    """Создать нового пользователя"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_data: UserCreate) -> User:
        if not user_data.password or len(user_data.password) < 6:
            raise ValidationError(
                field="password",
                message="Password is required and must be at least 6 characters",
                value=user_data.password
            )
        
        existing_email = self.repository.get_by_email(user_data.email)
        if existing_email:
            raise UniqueConstraintError("User", "email", user_data.email)
        
        existing_username = self.repository.get_by_username(user_data.username)
        if existing_username:
            raise UniqueConstraintError("User", "username", user_data.username)
        
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
