from typing import List, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.database import SessionLocal

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий с общими методами"""

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    @abstractmethod
    def _row_to_entity(self, row) -> T:
        """Преобразовать строку из БД в модель"""
        pass

    @abstractmethod
    def _get_table_name(self) -> str:
        """Вернуть имя таблицы"""
        pass

    @abstractmethod
    def _get_columns(self) -> list:
        """Вернуть список колонок для INSERT/UPDATE"""
        pass

    def get_all(self) -> List[T]:
        """Получить все записи"""
        from sqlalchemy import text

        columns_str = ", ".join(self._get_columns())
        query = text(f"SELECT id, {columns_str} FROM {self._get_table_name()}")
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, entity_id: int) -> Optional[T]:
        from sqlalchemy import text

        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE id = :id"
        )
        result = self.db.execute(query, {"id": entity_id})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def create(self, entity: T) -> T:
        columns = self._get_columns()
        placeholders = ", ".join([f":{col}" for col in columns])
        columns_str = ", ".join(columns)

        values = {col: getattr(entity, col) for col in columns}

        from sqlalchemy import text

        query = text(f"""
            INSERT INTO {self._get_table_name()} ({columns_str}) 
            VALUES ({placeholders})
            RETURNING id
        """)

        result = self.db.execute(query, values)
        self.db.commit()

        row = result.fetchone()
        if row:
            entity.id = row[0]

        return entity

    def update(self, entity_id: int, entity: T) -> Optional[T]:
        columns = self._get_columns()
        set_clause = ", ".join([f"{col} = :{col}" for col in columns])

        from sqlalchemy import text

        query = text(f"""
            UPDATE {self._get_table_name()} 
            SET {set_clause} 
            WHERE id = :id
        """)

        values = {col: getattr(entity, col) for col in columns}
        values["id"] = entity_id
        result = self.db.execute(query, values)
        self.db.commit()

        if result.rowcount > 0:
            entity.id = entity_id
            return entity
        return None

    def delete(self, entity_id: int) -> bool:
        from sqlalchemy import text

        query = text(f"DELETE FROM {self._get_table_name()} WHERE id = :id")
        result = self.db.execute(query, {"id": entity_id})
        self.db.commit()
        return result.rowcount > 0
