from typing import Optional
from src.schemas.category import Category, CategoryUpdate
from src.repositories.category_repository import CategoryRepository
from src.exceptions import NotFoundError, UniqueConstraintError


class UpdateCategoryUseCase:
    """Обновить категорию"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, category_id: int, category_data: CategoryUpdate) -> Category:
        existing_category = self.repository.get_by_id(category_id)
        if not existing_category:
            raise NotFoundError("Category", category_id)
        
        if category_data.title and category_data.title != existing_category.title:
            title_exists = self.repository.get_by_title(category_data.title)
            if title_exists:
                raise UniqueConstraintError("Category", "title", category_data.title)
        
        if category_data.slug and category_data.slug != existing_category.slug:
            slug_exists = self.repository.get_by_slug(category_data.slug)
            if slug_exists:
                raise UniqueConstraintError("Category", "slug", category_data.slug)
        
        updated_category = Category(
            id=category_id,
            title=category_data.title if category_data.title is not None else existing_category.title,
            description=category_data.description if category_data.description is not None else existing_category.description,
            slug=category_data.slug if category_data.slug is not None else existing_category.slug,
            is_published=category_data.is_published if category_data.is_published is not None else existing_category.is_published,
            created_at=existing_category.created_at
        )
        
        return self.repository.update(category_id, updated_category)
