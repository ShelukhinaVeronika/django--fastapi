from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.users import User, UserCreate, UserUpdate
from src.repositories.user_repository import UserRepository
from src.use_cases.user import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase
)
from src.exceptions import (
    NotFoundError, UniqueConstraintError, ValidationError,
    NotFoundHTTPError, ConflictHTTPError, BadRequestHTTPError
)


router = APIRouter(prefix="/users", tags=["Users"])

def get_user_repository():
    return UserRepository("db.sqlite3")


@router.get("/", response_model=List[User])
def get_all_users(
    skip: int = 0, 
    limit: int = 100,
    only_active: bool = False
):
    """Получить всех пользователей"""
    repository = get_user_repository()
    use_case = GetAllUsersUseCase(repository)
    return use_case.execute(skip, limit, only_active)


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    """Получить пользователя по ID"""
    repository = get_user_repository()
    use_case = GetUserByIdUseCase(repository)
    try:
        return use_case.execute(user_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Создать нового пользователя"""
    repository = get_user_repository()
    use_case = CreateUserUseCase(repository)
    
    try:
        return use_case.execute(user_data)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate):
    """Обновить пользователя"""
    repository = get_user_repository()
    use_case = UpdateUserUseCase(repository)
    
    try:
        return use_case.execute(user_id, user_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Удалить пользователя"""
    repository = get_user_repository()
    use_case = DeleteUserUseCase(repository)
    try:
        result = use_case.execute(user_id)
        if not result:
            raise NotFoundHTTPError("User", user_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
