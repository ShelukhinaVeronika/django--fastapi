from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.post import Post
from src.exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError


class PostRepository(BaseRepository[Post]):
    """Репозиторий для работы с постами"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "blog_post"

    def _get_columns(self) -> list:
        return [
            "title",
            "text",
            "pub_date",
            "image",
            "author_id",
            "location_id",
            "category_id",
            "is_published",
            "created_at",
        ]

    def _row_to_entity(self, row) -> Post:
        """Преобразуем строку из БД в SQLAlchemy модель Post"""
        return Post(
            id=row[0],
            title=row[1],
            text=row[2],
            pub_date=row[3],
            image=row[4],
            author_id=row[5],
            location_id=row[6] if row[6] else None,
            category_id=row[7] if row[7] else None,
            is_published=bool(row[8]),
            created_at=row[9],
        )

    def get_by_author(self, author_id: int) -> List[Post]:
        """Получить посты автора"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE author_id = :author_id
        """)
        result = self.db.execute(query, {"author_id": author_id})
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_category(self, category_id: int) -> List[Post]:
        """Получить посты категории"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE category_id = :category_id
        """)
        result = self.db.execute(query, {"category_id": category_id})
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_location(self, location_id: int) -> List[Post]:
        """Получить посты локации"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE location_id = :location_id
        """)
        result = self.db.execute(query, {"location_id": location_id})
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_published_posts(self) -> List[Post]:
        """Получить только опубликованные посты"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE is_published = TRUE
        """)
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_posts_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Post]:
        """Получить посты за период"""
        columns_str = ", ".join(self._get_columns())
        query = text(f"""
            SELECT id, {columns_str} 
            FROM {self._get_table_name()} 
            WHERE pub_date BETWEEN :start_date AND :end_date
        """)
        result = self.db.execute(
            query, {"start_date": start_date, "end_date": end_date}
        )
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, post_id: int) -> Post:
        post = super().get_by_id(post_id)
        if not post:
            raise NotFoundError("Post", post_id)
        return post

    def create(self, entity: Post) -> Post:
        try:
            return super().create(entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "slug" in error_msg:
                    raise UniqueConstraintError("Post", "slug", entity.slug)
                else:
                    raise UniqueConstraintError("Post", "unknown", str(e))
            if (
                "FOREIGN KEY constraint" in error_msg
                or "violates foreign key constraint" in error_msg
            ):
                if "author_id" in error_msg:
                    raise ForeignKeyError("User", "author_id", entity.author_id)
                elif "category_id" in error_msg:
                    raise ForeignKeyError("Category", "category_id", entity.category_id)
                elif "location_id" in error_msg:
                    raise ForeignKeyError("Location", "location_id", entity.location_id)
            raise

    def update(self, post_id: int, entity: Post) -> Post:
        self.get_by_id(post_id)
        try:
            result = super().update(post_id, entity)
            return result
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "slug" in error_msg:
                    raise UniqueConstraintError("Post", "slug", entity.slug)
                else:
                    raise UniqueConstraintError("Post", "unknown", str(e))
            if (
                "FOREIGN KEY constraint" in error_msg
                or "violates foreign key constraint" in error_msg
            ):
                if "author_id" in error_msg:
                    raise ForeignKeyError("User", "author_id", entity.author_id)
                elif "category_id" in error_msg:
                    raise ForeignKeyError("Category", "category_id", entity.category_id)
                elif "location_id" in error_msg:
                    raise ForeignKeyError("Location", "location_id", entity.location_id)
            raise

    def delete(self, post_id: int) -> bool:
        self.get_by_id(post_id)
        return super().delete(post_id)
