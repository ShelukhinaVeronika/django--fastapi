from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.schemas.users import User


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями (таблица auth_user)"""
    
    def _get_table_name(self) -> str:
        return "auth_user"
    
    def _get_columns(self) -> list:
        return [
            "username", "email", "first_name", "last_name", 
            "password", "is_active", "is_superuser", "is_staff", 
            "date_joined", "last_login"
        ]
    
    def _row_to_entity(self, row) -> User:
        return User(
            id=row[0],
            password=row[1],
            last_login=row[2],
            is_superuser=bool(row[3]),
            username=row[4],
            last_name=row[5],
            email=row[6] if row[6] else None,
            is_staff=bool(row[7]),
            is_active=bool(row[8]),
            date_joined=row[9],
            first_name=row[10]
        )
    
    def get_by_email(self, email: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def get_active_users(self) -> List[User]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self._get_table_name()} WHERE is_active = 1"
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]