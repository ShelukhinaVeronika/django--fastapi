from src.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    """Удалить комментарий"""
    
    def __init__(self, repository: CommentRepository):
        self.repository = repository
    
    def execute(self, comment_id: int) -> bool:
        return self.repository.delete(comment_id)