from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.category import Category
from src.exceptions import NotFoundError, UniqueConstraintError


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "blog_category"

    def _get_columns(self) -> list:
        return ["title", "description", "slug", "is_published", "created_at"]

    def _row_to_entity(self, row) -> Category:
        """Преобразуем строку из БД в SQLAlchemy модель Category"""
        return Category(
            id=row[0],
            title=row[1],
            description=row[2],
            slug=row[3],
            is_published=bool(row[4]),
            created_at=row[5],
        )

    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE slug = :slug"
        )
        result = self.db.execute(query, {"slug": slug})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def get_by_title(self, title: str) -> Optional[Category]:
        """Получить категорию по названию"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE title = :title"
        )
        result = self.db.execute(query, {"title": title})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def get_published(self) -> List[Category]:
        """Получить только опубликованные категории"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE is_published = TRUE"
        )
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, category_id: int) -> Category:
        category = super().get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", category_id)
        return category

    def create(self, entity: Category) -> Category:
        try:
            return super().create(entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "title" in error_msg:
                    raise UniqueConstraintError("Category", "title", entity.title)
                elif "slug" in error_msg:
                    raise UniqueConstraintError("Category", "slug", entity.slug)
                else:
                    raise UniqueConstraintError("Category", "unknown", str(e))
            raise

    def update(self, category_id: int, entity: Category) -> Category:
        self.get_by_id(category_id)
        try:
            return super().update(category_id, entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "title" in error_msg:
                    raise UniqueConstraintError("Category", "title", entity.title)
                elif "slug" in error_msg:
                    raise UniqueConstraintError("Category", "slug", entity.slug)
                else:
                    raise UniqueConstraintError("Category", "unknown", str(e))
            raise

    def delete(self, category_id: int) -> bool:
        self.get_by_id(category_id)
        return super().delete(category_id)
