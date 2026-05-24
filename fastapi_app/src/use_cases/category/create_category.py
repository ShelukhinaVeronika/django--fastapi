from typing import Optional
from src.schemas.category import Category, CategoryCreate
from src.repositories.category_repository import CategoryRepository
from src.exceptions import UniqueConstraintError


class CreateCategoryUseCase:
    """Создать новую категорию"""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category_data: CategoryCreate) -> Category:
        existing_by_title = self.repository.get_by_title(category_data.title)
        if existing_by_title:
            raise UniqueConstraintError("Category", "title", category_data.title)

        existing_by_slug = self.repository.get_by_slug(category_data.slug)
        if existing_by_slug:
            raise UniqueConstraintError("Category", "slug", category_data.slug)

        new_category = Category(
            title=category_data.title,
            description=category_data.description,
            slug=category_data.slug,
            is_published=category_data.is_published,
            created_at=category_data.created_at,
        )

        return self.repository.create(new_category)
