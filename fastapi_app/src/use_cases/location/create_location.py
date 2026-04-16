from src.schemas.location import Location, LocationCreate
from src.repositories.location_repository import LocationRepository


class CreateLocationUseCase:
    """Создать новую локацию"""
    
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def execute(self, location_data: LocationCreate) -> Location:
        new_location = Location(
            name=location_data.name,
            is_published=location_data.is_published,
            created_at=location_data.created_at
        )
        
        return self.repository.create(new_location)