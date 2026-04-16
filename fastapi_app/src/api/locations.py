from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.repositories.location_repository import LocationRepository
from src.use_cases.location import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetAllLocationsUseCase,
    GetLocationByIdUseCase,
    UpdateLocationUseCase
)

router = APIRouter(prefix="/locations", tags=["Locations"])

def get_location_repository():
    return LocationRepository("db.sqlite3")


@router.get("/", response_model=List[Location])
def get_all_locations(
    skip: int = 0, 
    limit: int = 100,
    only_published: bool = False
):
    """Получить все локации"""
    repository = get_location_repository()
    use_case = GetAllLocationsUseCase(repository)
    return use_case.execute(skip, limit, only_published)


@router.get("/{location_id}", response_model=Location)
def get_location_by_id(location_id: int):
    """Получить локацию по ID"""
    repository = get_location_repository()
    use_case = GetLocationByIdUseCase(repository)
    location = use_case.execute(location_id)
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    return location


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
def create_location(location_data: LocationCreate):
    """Создать новую локацию"""
    repository = get_location_repository()
    use_case = CreateLocationUseCase(repository)
    return use_case.execute(location_data)


@router.put("/{location_id}", response_model=Location)
def update_location(location_id: int, location_data: LocationUpdate):
    """Обновить локацию"""
    repository = get_location_repository()
    use_case = UpdateLocationUseCase(repository)
    
    location = use_case.execute(location_id, location_data)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int):
    """Удалить локацию"""
    repository = get_location_repository()
    use_case = DeleteLocationUseCase(repository)
    
    deleted = use_case.execute(location_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    return None