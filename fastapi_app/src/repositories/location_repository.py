from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.schemas.location import Location


class LocationRepository(BaseRepository[Location]):
    """Репозиторий для работы с локациями"""
    
    def _get_table_name(self) -> str:
        return "blog_location"
    
    def _get_columns(self) -> list:
        return ["name", "is_published", "created_at"]
    
    def _row_to_entity(self, row) -> Location:
        """Преобразуем строку SQLite в Pydantic модель Location"""
        return Location(
            id=row[0],
            name=row[1],
            is_published=bool(row[2]),
            created_at=row[3]
        )
    
    def get_published(self) -> List[Location]:
        """Получить только опубликованные локации"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE is_published = 1"
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]