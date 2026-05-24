from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.location import Location
from src.exceptions import NotFoundError, UniqueConstraintError


class LocationRepository(BaseRepository[Location]):
    """Репозиторий для работы с локациями"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "blog_location"

    def _get_columns(self) -> list:
        return ["name", "is_published", "created_at"]

    def _row_to_entity(self, row) -> Location:
        """Преобразуем строку из БД в SQLAlchemy модель Location"""
        return Location(
            id=row[0], name=row[1], is_published=bool(row[2]), created_at=row[3]
        )

    def get_by_name(self, name: str) -> Optional[Location]:
        """Получить локацию по названию"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE name = :name"
        )
        result = self.db.execute(query, {"name": name})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def get_published(self) -> List[Location]:
        """Получить только опубликованные локации"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE is_published = TRUE"
        )
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, location_id: int) -> Location:
        location = super().get_by_id(location_id)
        if not location:
            raise NotFoundError("Location", location_id)
        return location

    def create(self, entity: Location) -> Location:
        try:
            return super().create(entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                raise UniqueConstraintError("Location", "name", entity.name)
            raise

    def update(self, location_id: int, entity: Location) -> Location:
        self.get_by_id(location_id)
        try:
            return super().update(location_id, entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                raise UniqueConstraintError("Location", "name", entity.name)
            raise

    def delete(self, location_id: int) -> bool:
        self.get_by_id(location_id)
        return super().delete(location_id)
