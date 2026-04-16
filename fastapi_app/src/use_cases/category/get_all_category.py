from typing import List, Optional
from src.schemas.category import Category
from src.repositories.category_repository import CategoryRepository


class GetAllCategoriesUseCase:
    """Получить все категории"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, skip: int = 0, limit: int = 100, only_published: bool = False) -> List[Category]:
        if only_published:
            categories = self.repository.get_published()
        else:
            categories = self.repository.get_all()
        
        return categories[skip:skip + limit]