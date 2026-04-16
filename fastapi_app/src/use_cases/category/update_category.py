from typing import Optional
from src.schemas.category import Category, CategoryUpdate
from src.repositories.category_repository import CategoryRepository


class UpdateCategoryUseCase:
    """Обновить категорию"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        existing_category = self.repository.get_by_id(category_id)
        if not existing_category:
            return None
        
        if category_data.slug and category_data.slug != existing_category.slug:
            slug_exists = self.repository.get_by_slug(category_data.slug)
            if slug_exists:
                raise ValueError(f"Category with slug '{category_data.slug}' already exists")
        
        updated_category = Category(
            id=category_id,
            title=category_data.title if category_data.title is not None else existing_category.title,
            description=category_data.description if category_data.description is not None else existing_category.description,
            slug=category_data.slug if category_data.slug is not None else existing_category.slug,
            is_published=category_data.is_published if category_data.is_published is not None else existing_category.is_published,
            created_at=existing_category.created_at
        )
        
        return self.repository.update(category_id, updated_category)