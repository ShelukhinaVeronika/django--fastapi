from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.sql import func
from src.database import Base


class PublishedMixin:
    is_published = Column(Boolean, default=True, nullable=False)


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
