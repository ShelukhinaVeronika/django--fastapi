from typing import List
from src.schemas.location import Location
from src.repositories.location_repository import LocationRepository


class GetAllLocationsUseCase:
    """Получить все локации"""
    
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def execute(self, skip: int = 0, limit: int = 100, only_published: bool = False) -> List[Location]:
        if only_published:
            locations = self.repository.get_published()
        else:
            locations = self.repository.get_all()
        
        return locations[skip:skip + limit]