import sqlite3
from typing import List, Optional, TypeVar, Generic, Any
from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий с общими методами"""
    
    def __init__(self, db_path: str = "db.sqlite3"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Получить соединение с БД"""
        return sqlite3.connect(self.db_path)
    
    @abstractmethod
    def _row_to_entity(self, row) -> T:
        """Преобразовать строку из БД в Pydantic модель"""
        pass
    
    @abstractmethod
    def _get_table_name(self) -> str:
        """Вернуть имя таблицы"""
        pass
    
    @abstractmethod
    def _get_columns(self) -> list:
        """Вернуть список колонок для INSERT/UPDATE (без id и created_at)"""
        pass
    
    def get_all(self) -> List[T]:
        """Получить все записи"""
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {self._get_table_name()}")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить запись по ID"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE id = ?",
                (entity_id,)
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def create(self, entity: T) -> T:
        """Создать новую запись"""
        columns = self._get_columns()
        placeholders = ','.join(['?' for _ in columns])
        columns_str = ','.join(columns)
        
        values = [getattr(entity, col) for col in columns]
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"INSERT INTO {self._get_table_name()} ({columns_str}) VALUES ({placeholders})",
                values
            )
            conn.commit()
            entity.id = cursor.lastrowid
            return entity
    
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        """Обновить запись"""
        columns = self._get_columns()
        set_clause = ','.join([f"{col} = ?" for col in columns])
        
        values = [getattr(entity, col) for col in columns]
        values.append(entity_id)
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE {self._get_table_name()} SET {set_clause} WHERE id = ?",
                values
            )
            conn.commit()
            if cursor.rowcount > 0:
                entity.id = entity_id
                return entity
            return None
    
    def delete(self, entity_id: int) -> bool:
        """Удалить запись"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"DELETE FROM {self._get_table_name()} WHERE id = ?",
                (entity_id,)
            )
            conn.commit()
            return cursor.rowcount > 0