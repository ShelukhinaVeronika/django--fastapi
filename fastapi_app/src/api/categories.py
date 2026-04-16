from fastapi import APIRouter, HTTPException, status
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
    category = use_case.execute(category_id)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return category


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate):
    """Создать новую категорию"""
    repository = get_category_repository()
    use_case = CreateCategoryUseCase(repository)
    
    try:
        category = use_case.execute(category_data)
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category_data: CategoryUpdate):
    """Обновить категорию"""
    repository = get_category_repository()
    use_case = UpdateCategoryUseCase(repository)
    
    try:
        category = use_case.execute(category_id, category_data)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    """Удалить категорию"""
    repository = get_category_repository()
    use_case = DeleteCategoryUseCase(repository)
    
    deleted = use_case.execute(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return None