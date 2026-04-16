from typing import List, Optional
from src.schemas.comments import Comment
from src.repositories.comment_repository import CommentRepository


class GetAllCommentsUseCase:
    """Получить все комментарии"""
    
    def __init__(self, repository: CommentRepository):
        self.repository = repository
    
    def execute(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        post_id: Optional[int] = None,
        only_published: bool = False
    ) -> List[Comment]:

        if post_id:
            comments = self.repository.get_by_post(post_id)
        elif only_published:
            comments = self.repository.get_published()
        else:
            comments = self.repository.get_all()
        
        return comments[skip:skip + limit]