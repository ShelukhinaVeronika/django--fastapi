from typing import Optional
from src.schemas.users import User, UserUpdate
from src.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    """Обновить пользователя"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            return None
        
        if user_data.email and user_data.email != existing_user.email:
            email_exists = self.repository.get_by_email(user_data.email)
            if email_exists:
                raise ValueError(f"User with email '{user_data.email}' already exists")
        
        if user_data.username and user_data.username != existing_user.username:
            username_exists = self.repository.get_by_username(user_data.username)
            if username_exists:
                raise ValueError(f"User with username '{user_data.username}' already exists")
        
        updated_user = User(
    id=user_id,
    username=user_data.username if user_data.username is not None else existing_user.username,
    email=user_data.email if user_data.email is not None else existing_user.email,
    first_name=user_data.first_name if user_data.first_name is not None else existing_user.first_name,
    last_name=user_data.last_name if user_data.last_name is not None else existing_user.last_name,
    password=user_data.password if user_data.password is not None else existing_user.password,
    is_active=user_data.is_active if user_data.is_active is not None else existing_user.is_active,
    is_superuser=user_data.is_superuser if user_data.is_superuser is not None else existing_user.is_superuser,
    is_staff=user_data.is_staff if user_data.is_staff is not None else existing_user.is_staff,
    date_joined=existing_user.date_joined,
    last_login=existing_user.last_login
)
        
        return self.repository.update(user_id, updated_user)