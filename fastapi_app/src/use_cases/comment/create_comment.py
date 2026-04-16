from src.schemas.comments import Comment, CommentCreate
from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository


class CreateCommentUseCase:
    """Создать новый комментарий"""
    
    def __init__(self, repository: CommentRepository, post_repository: PostRepository):
        self.repository = repository
        self.post_repository = post_repository
    
    def execute(self, comment_data: CommentCreate) -> Comment:
        post = self.post_repository.get_by_id(comment_data.post_id)
        if not post:
            raise ValueError(f"Post with id {comment_data.post_id} does not exist")
        
        new_comment = Comment(
            text=comment_data.text,
            post_id=comment_data.post_id,
            author_id=comment_data.author_id,
            is_published=comment_data.is_published,
            created_at=comment_data.created_at
        )
        
        return self.repository.create(new_comment)