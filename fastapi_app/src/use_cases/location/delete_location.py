from src.repositories.location_repository import LocationRepository


class DeleteLocationUseCase:
    """Удалить локацию"""
    
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def execute(self, location_id: int) -> bool:
        return self.repository.delete(location_id)