from typing import Optional
from src.schemas.location import Location
from src.repositories.location_repository import LocationRepository


class GetLocationByIdUseCase:
    """Получить локацию по ID"""
    
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def execute(self, location_id: int) -> Optional[Location]:
        return self.repository.get_by_id(location_id)