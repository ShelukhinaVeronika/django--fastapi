from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.comment import Comment
from src.exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError


class CommentRepository(BaseRepository[Comment]):
    """Репозиторий для работы с комментариями"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "blog_comment"

    def _get_columns(self) -> list:
        return ["text", "image", "post_id", "author_id", "is_published", "created_at"]

    def _row_to_entity(self, row) -> Comment:
        """Преобразуем строку из БД в SQLAlchemy модель Comment"""
        return Comment(
            id=row[0],
            text=row[1],
            image=row[2] if row[2] else None,
            post_id=row[3],
            author_id=row[4],
            is_published=bool(row[5]),
            created_at=row[6],
        )

    def get_by_post(self, post_id: int) -> List[Comment]:
        """Получить комментарии поста"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE post_id = :post_id 
            ORDER BY created_at
        """)
        result = self.db.execute(query, {"post_id": post_id})
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_author(self, author_id: int) -> List[Comment]:
        """Получить комментарии автора"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE author_id = :author_id
        """)
        result = self.db.execute(query, {"author_id": author_id})
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_published(self) -> List[Comment]:
        """Получить опубликованные комментарии"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE is_published = TRUE
        """)
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, comment_id: int) -> Comment:
        comment = super().get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment", comment_id)
        return comment

    def create(self, entity: Comment) -> Comment:
        print(f"💾💾💾 REPOSITORY CREATE: entity.image = {entity.image}")
        try:
            return super().create(entity)
        except Exception as e:
            print(f"💾💾💾 ERROR: {e}")
            raise

    def update(self, comment_id: int, entity: Comment) -> Comment:
        self.get_by_id(comment_id)
        result = super().update(comment_id, entity)
        return result

    def delete(self, comment_id: int) -> bool:
        self.get_by_id(comment_id)
        return super().delete(comment_id)
