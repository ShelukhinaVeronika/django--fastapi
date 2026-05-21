from fastapi import APIRouter, HTTPException, status, Depends
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
from src.exceptions import (
    NotFoundError, UniqueConstraintError, ValidationError,
    NotFoundHTTPError, ConflictHTTPError, BadRequestHTTPError
)
from src.auth.dependencies import get_current_user
from src.schemas.users import User 


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
    try:
        return use_case.execute(location_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
def create_location(location_data: LocationCreate,
                    current_user: User = Depends(get_current_user)):
    """Создать новую локацию"""

    repository = get_location_repository()
    use_case = CreateLocationUseCase(repository)
    try:
        return use_case.execute(location_data)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.put("/{location_id}", response_model=Location)
def update_location(location_id: int, location_data: LocationUpdate,
                    current_user: User = Depends(get_current_user)):
    """Обновить локацию"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    repository = get_location_repository()
    use_case = UpdateLocationUseCase(repository)
    
    try:
        return use_case.execute(location_id, location_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int,
                    current_user: User = Depends(get_current_user)):
    """Удалить локацию"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    repository = get_location_repository()
    use_case = DeleteLocationUseCase(repository)
    try:
        result = use_case.execute(location_id)
        if not result:
            raise NotFoundHTTPError("Location", location_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
