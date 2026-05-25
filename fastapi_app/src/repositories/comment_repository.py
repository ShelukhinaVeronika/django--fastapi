from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.comment import Comment
from src.exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError
from src.repositories.image_repository import ImageRepository

class CommentRepository(BaseRepository[Comment]):
    """Репозиторий для работы с комментариями"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "blog_comment"

    def _get_columns(self) -> list:
        return ["text", "post_id", "author_id", "is_published", "created_at"]

    def _row_to_entity(self, row) -> Comment:
        """Преобразуем строку из БД в SQLAlchemy модель Comment"""
        return Comment(
            id=row[0],
            text=row[1],
            post_id=row[2],
            author_id=row[3],
            is_published=bool(row[4]),
            created_at=row[5],
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
        comments = [self._row_to_entity(row) for row in rows]
        image_repo = ImageRepository(self.db)
        for comment in comments:    
            images = image_repo.get_by_comment(comment.id)
            comment.images = [img.url for img in images]
    
        return comments

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
        try:
            return super().create(entity)
        except Exception as e:
            error_msg = str(e)
        if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
            raise UniqueConstraintError("Comment", "id", str(entity.id))
        if "FOREIGN KEY constraint" in error_msg or "violates foreign key constraint" in error_msg:
            if "post_id" in error_msg:
                raise ForeignKeyError("Post", "post_id", entity.post_id)
            if "author_id" in error_msg:
                raise ForeignKeyError("User", "author_id", entity.author_id)
            raise

    def update(self, comment_id: int, entity: Comment) -> Comment:
        self.get_by_id(comment_id)
        result = super().update(comment_id, entity)
        return result

    def delete(self, comment_id: int) -> bool:
        self.get_by_id(comment_id)
        return super().delete(comment_id)
