from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.schemas.users import User, UserCreate, UserUpdate
from src.repositories.user_repository import UserRepository
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.use_cases.user import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
)
from src.exceptions import (
    NotFoundError,
    UniqueConstraintError,
    ValidationError,
    NotFoundHTTPError,
    ConflictHTTPError,
    BadRequestHTTPError,
)
from src.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_post_repository(db: Session = Depends(get_db)):
    return PostRepository(db)


def get_comment_repository(db: Session = Depends(get_db)):
    return CommentRepository(db)


@router.get("/", response_model=List[User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    only_active: bool = False,
    db: Session = Depends(get_db),
):
    """Получить всех пользователей"""
    repository = get_user_repository(db)
    use_case = GetAllUsersUseCase(repository)
    return use_case.execute(skip, limit, only_active)


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    repository = get_user_repository(db)
    use_case = GetUserByIdUseCase(repository)
    try:
        return use_case.execute(user_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    repository = get_user_repository(db)
    use_case = CreateUserUseCase(repository)

    try:
        return use_case.execute(user_data)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Удалить текущего пользователя и все его посты и комментарии"""
    user_repository = get_user_repository(db)
    post_repository = get_post_repository(db)
    comment_repository = get_comment_repository(db)

    use_case = DeleteUserUseCase(user_repository, post_repository, comment_repository)

    try:
        result = use_case.execute(current_user.id)
        if not result:
            raise NotFoundHTTPError("User", current_user.id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить пользователя (только для админов)"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")

    repository = get_user_repository(db)
    use_case = UpdateUserUseCase(repository)

    try:
        return use_case.execute(user_id, user_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить пользователя (только для админов)"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")

    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")

    user_repository = get_user_repository(db)
    post_repository = get_post_repository(db)
    comment_repository = get_comment_repository(db)

    use_case = DeleteUserUseCase(user_repository, post_repository, comment_repository)

    try:
        result = use_case.execute(user_id)
        if not result:
            raise NotFoundHTTPError("User", user_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
