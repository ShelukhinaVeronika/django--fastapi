from typing import Optional
from src.schemas.comments import Comment
from src.repositories.comment_repository import CommentRepository


class GetCommentByIdUseCase:
    """Получить комментарий по ID"""
    
    def __init__(self, repository: CommentRepository):
        self.repository = repository
    
    def execute(self, comment_id: int) -> Optional[Comment]:
        return self.repository.get_by_id(comment_id)