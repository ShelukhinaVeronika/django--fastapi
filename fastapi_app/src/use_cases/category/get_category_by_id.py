from typing import Optional
from src.schemas.category import Category
from src.repositories.category_repository import CategoryRepository


class GetCategoryByIdUseCase:
    """Получить категорию по ID"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, category_id: int) -> Optional[Category]:
        return self.repository.get_by_id(category_id)