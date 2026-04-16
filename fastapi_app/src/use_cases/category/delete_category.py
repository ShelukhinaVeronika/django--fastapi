from src.repositories.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    """Удалить категорию"""
    
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, category_id: int) -> bool:
        return self.repository.delete(category_id)