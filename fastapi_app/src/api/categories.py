from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.repositories.category_repository import CategoryRepository
from src.use_cases.category import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetAllCategoriesUseCase,
    GetCategoryByIdUseCase,
    UpdateCategoryUseCase
)
from src.exceptions import (
    NotFoundError, UniqueConstraintError, ValidationError,
    NotFoundHTTPError, ConflictHTTPError, BadRequestHTTPError
)
from src.auth.dependencies import get_current_user
from src.schemas.users import User


router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_repository():
    return CategoryRepository("db.sqlite3")


@router.get("/", response_model=List[Category])
def get_all_categories(
    skip: int = 0, 
    limit: int = 100,
    only_published: bool = False
):
    """Получить все категории"""
    repository = get_category_repository()
    use_case = GetAllCategoriesUseCase(repository)
    return use_case.execute(skip, limit, only_published)


@router.get("/{category_id}", response_model=Category)
def get_category_by_id(category_id: int):
    """Получить категорию по ID"""
    repository = get_category_repository()
    use_case = GetCategoryByIdUseCase(repository)
    
    try:
        return use_case.execute(category_id);
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate,
                    current_user: User = Depends(get_current_user)):
    """Создать новую категорию"""
    repository = get_category_repository()
    use_case = CreateCategoryUseCase(repository)
    
    try:
        return use_case.execute(category_data)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
         raise BadRequestHTTPError(e.message, e.field)


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category_data: CategoryUpdate,
                    current_user: User = Depends(get_current_user)):
    """Обновить категорию"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    repository = get_category_repository()
    use_case = UpdateCategoryUseCase(repository)
    
    try:
        return use_case.execute(category_id, category_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int,
                    current_user: User = Depends(get_current_user)):
    """Удалить категорию"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    repository = get_category_repository()
    use_case = DeleteCategoryUseCase(repository)
    try:
        result = use_case.execute(category_id)
        if not result:
            raise NotFoundHTTPError("Category", category_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
