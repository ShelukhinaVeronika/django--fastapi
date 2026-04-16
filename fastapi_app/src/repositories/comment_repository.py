from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.schemas.comments import Comment


class CommentRepository(BaseRepository[Comment]):
    """Репозиторий для работы с комментариями"""
    
    def _get_table_name(self) -> str:
        return "blog_comment"
    
    def _get_columns(self) -> list:
        return ["text", "post_id", "author_id", "created_at", "is_published"]
    
    def _row_to_entity(self, row) -> Comment:
        """Преобразуем строку SQLite в Pydantic модель Comment"""
        return Comment(
            id=row[0],
            text=row[1],
            created_at=row[2],
            author_id=row[3],
            post_id=row[4],
            is_published=bool(row[5])
        )
    
    def get_by_post(self, post_id: int) -> List[Comment]:
        """Получить комментарии поста"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE post_id = ? ORDER BY created_at",
                (post_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_author(self, author_id: int) -> List[Comment]:
        """Получить комментарии автора"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE author_id = ?",
                (author_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_published(self) -> List[Comment]:
        """Получить опубликованные комментарии"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE is_published = 1"
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]