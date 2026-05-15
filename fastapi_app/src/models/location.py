from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from .base import PublishedMixin, TimestampMixin


class Location(Base, PublishedMixin, TimestampMixin):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)

    posts = relationship("Post", back_populates="location")
