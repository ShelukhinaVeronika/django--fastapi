from fastapi import APIRouter, HTTPException, status, Depends
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
from src.auth.dependencies import get_current_user


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


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Обновить текущего пользователя"""
    repository = get_user_repository()
    use_case = UpdateUserUseCase(repository)
    
    try:
        return use_case.execute(current_user.id, user_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    current_user: User = Depends(get_current_user)
):
    """Удалить текущего пользователя"""
    repository = get_user_repository()
    use_case = DeleteUserUseCase(repository)
    
    try:
        result = use_case.execute(current_user.id)
        if not result:
            raise NotFoundHTTPError("User", current_user.id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)



@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate,
                current_user: User = Depends(get_current_user)):
    """Обновить пользователя"""

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")

    repository = get_user_repository()
    use_case = UpdateUserUseCase(repository)
    
    try:
        return use_case.execute(user_id, user_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                current_user: User = Depends(get_current_user)):
    """Удалить пользователя"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    repository = get_user_repository()
    use_case = DeleteUserUseCase(repository)
    try:
        result = use_case.execute(user_id)
        if not result:
            raise NotFoundHTTPError("User", user_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
