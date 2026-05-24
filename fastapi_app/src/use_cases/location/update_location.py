from typing import Optional
from src.schemas.location import Location, LocationUpdate
from src.repositories.location_repository import LocationRepository
from src.exceptions import NotFoundError, UniqueConstraintError


class UpdateLocationUseCase:
    """Обновить локацию"""

    def __init__(self, repository: LocationRepository):
        self.repository = repository

    def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        existing_location = self.repository.get_by_id(location_id)
        if not existing_location:
            raise NotFoundError("Location", location_id)
        if location_data.name and location_data.name != existing_location.name:
            name_exists = self.repository.get_by_name(location_data.name)
            if name_exists:
                raise UniqueConstraintError("Location", "name", location_data.name)

        updated_location = Location(
            id=location_id,
            name=(
                location_data.name
                if location_data.name is not None
                else existing_location.name
            ),
            is_published=(
                location_data.is_published
                if location_data.is_published is not None
                else existing_location.is_published
            ),
            created_at=existing_location.created_at,
        )

        return self.repository.update(location_id, updated_location)
