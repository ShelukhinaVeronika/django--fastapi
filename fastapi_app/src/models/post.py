from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base
from .base import PublishedMixin, TimestampMixin


class Post(Base, PublishedMixin, TimestampMixin):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    image = Column(String(500), nullable=True)

    author_id = Column(Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("blog_location.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(Integer, ForeignKey("blog_category.id", ondelete="SET NULL"), nullable=True)

    author = relationship("User", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
