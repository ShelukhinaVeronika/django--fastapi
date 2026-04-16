from typing import List, Optional
from datetime import datetime
from src.repositories.base_repository import BaseRepository
from src.schemas.posts import Post


class PostRepository(BaseRepository[Post]):
    """Репозиторий для работы с постами"""
    
    def _get_table_name(self) -> str:
        return "blog_post"
    
    def _get_columns(self) -> list:
        return ["title", "text", "pub_date", "author_id", "location_id", 
                "category_id", "image", "is_published", "created_at"]
    
    def _row_to_entity(self, row) -> Post:
        """Преобразуем строку SQLite в Pydantic модель Post"""
        return Post(
            id=row[0],
            title=row[1],
            text=row[2],
            pub_date=row[3],
            is_published=bool(row[4]),
            created_at=row[5],
            author_id=row[6],
            category_id=row[7],
            location_id=row[8],
            image=row[9]
        )
    
    def get_by_author(self, author_id: int) -> List[Post]:
        """Получить посты автора"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE author_id = ?",
                (author_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_category(self, category_id: int) -> List[Post]:
        """Получить посты категории"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE category_id = ?",
                (category_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_location(self, location_id: int) -> List[Post]:
        """Получить посты локации"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE location_id = ?",
                (location_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_published_posts(self) -> List[Post]:
        """Получить только опубликованные посты"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE is_published = 1"
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_posts_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Post]:
        """Получить посты за период"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE pub_date BETWEEN ? AND ?",
                (start_date, end_date)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]