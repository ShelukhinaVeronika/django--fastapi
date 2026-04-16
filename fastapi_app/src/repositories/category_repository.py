from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.schemas.category import Category


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями"""
    
    def _get_table_name(self) -> str:
        return "blog_category"
    
    def _get_columns(self) -> list:
        return ["title", "description", "slug", "is_published", "created_at"]
    
    def _row_to_entity(self, row) -> Category:
        """Преобразуем строку SQLite в Pydantic модель Category"""
        return Category(
            id=row[0],
            title=row[1],
            description=row[2],
            slug=row[3],
            is_published=bool(row[4]),
            created_at=row[5]
        )
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE slug = ?",
                (slug,)
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def get_published(self) -> List[Category]:
        """Получить только опубликованные категории"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE is_published = 1"
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]