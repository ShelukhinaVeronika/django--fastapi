from typing import Optional
from src.schemas.comments import Comment, CommentUpdate
from src.repositories.comment_repository import CommentRepository


class UpdateCommentUseCase:
    """Обновить комментарий"""
    
    def __init__(self, repository: CommentRepository):
        self.repository = repository
    
    def execute(self, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        existing_comment = self.repository.get_by_id(comment_id)
        if not existing_comment:
            return None
        
        updated_comment = Comment(
            id=comment_id,
            text=comment_data.text if comment_data.text is not None else existing_comment.text,
            post_id=existing_comment.post_id,
            author_id=existing_comment.author_id,
            is_published=comment_data.is_published if comment_data.is_published is not None else existing_comment.is_published,
            created_at=existing_comment.created_at
        )
        
        return self.repository.update(comment_id, updated_comment)