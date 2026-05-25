from typing import List
from sqlalchemy.orm import Session
from src.models.image import Image


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, url: str, post_id: int = None, comment_id: int = None) -> Image:
        image = Image(url=url, post_id=post_id, comment_id=comment_id)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
    
    def get_by_post(self, post_id: int) -> List[Image]:
        return self.db.query(Image).filter(Image.post_id == post_id).all()
    
    def get_by_comment(self, comment_id: int) -> List[Image]:
        return self.db.query(Image).filter(Image.comment_id == comment_id).all()
    
    def delete_by_post(self, post_id: int):
        self.db.query(Image).filter(Image.post_id == post_id).delete()
        self.db.commit()
    
    def delete_by_comment(self, comment_id: int):
        self.db.query(Image).filter(Image.comment_id == comment_id).delete()
        self.db.commit()
