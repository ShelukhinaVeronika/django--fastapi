from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database import Base
from .base import PublishedMixin, TimestampMixin


class Comment(Base, PublishedMixin, TimestampMixin):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    image = Column(String(500), nullable=True)
    post_id = Column(
        Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(
        Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False
    )

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    images = relationship("Image", back_populates="comment", cascade="all, delete-orphan")
