from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.repositories.base_repository import BaseRepository
from src.models.user import User
from src.exceptions import NotFoundError, UniqueConstraintError


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями (таблица auth_user)"""

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_table_name(self) -> str:
        return "auth_user"

    def _get_columns(self) -> list:
        return [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "date_joined",
            "last_login",
        ]

    def _row_to_entity(self, row) -> User:
        return User(
            id=row[0],
            username=row[1],
            email=row[2] if row[2] else None,
            first_name=row[3],
            last_name=row[4],
            password=row[5],
            is_active=bool(row[6]),
            is_superuser=bool(row[7]),
            is_staff=bool(row[8]),
            date_joined=row[9],
            last_login=row[10] if row[10] else None,
        )

    def get_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE email = :email"
        )
        result = self.db.execute(query, {"email": email})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def get_by_username(self, username: str) -> Optional[User]:
        """Получить пользователя по username"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE username = :username"
        )
        result = self.db.execute(query, {"username": username})
        row = result.fetchone()
        return self._row_to_entity(row) if row else None

    def get_active_users(self) -> List[User]:
        """Получить активных пользователей"""
        columns_str = ", ".join(self._get_columns())
        query = text(
            f"SELECT id, {columns_str} FROM {self._get_table_name()} WHERE is_active = TRUE"
        )
        result = self.db.execute(query)
        rows = result.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, user_id: int) -> User:
        user = super().get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    def create(self, entity: User) -> User:
        from src.auth.hashing import hash_password

        entity.password = hash_password(entity.password)
        try:
            return super().create(entity)
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "username" in error_msg:
                    raise UniqueConstraintError("User", "username", entity.username)
                elif "email" in error_msg:
                    raise UniqueConstraintError("User", "email", entity.email)
                else:
                    raise UniqueConstraintError("User", "unknown", str(e))
            raise

    def update(self, user_id: int, entity: User) -> User:
        self.get_by_id(user_id)
        try:
            result = super().update(user_id, entity)
            return result
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint" in error_msg or "duplicate key" in error_msg:
                if "username" in error_msg:
                    raise UniqueConstraintError("User", "username", entity.username)
                elif "email" in error_msg:
                    raise UniqueConstraintError("User", "email", entity.email)
                else:
                    raise UniqueConstraintError("User", "unknown", str(e))
            raise

    def delete(self, user_id: int) -> bool:
        self.get_by_id(user_id)
        return super().delete(user_id)
