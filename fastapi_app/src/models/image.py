from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from .base import TimestampMixin


class Image(Base, TimestampMixin):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    
    post_id = Column(Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=True)
    comment_id = Column(Integer, ForeignKey("blog_comment.id", ondelete="CASCADE"), nullable=True)

    post = relationship("Post", back_populates="images")
    comment = relationship("Comment", back_populates="images")
    