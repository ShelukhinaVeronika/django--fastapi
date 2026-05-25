from src.schemas.comments import Comment
from src.repositories.comment_repository import CommentRepository
from src.repositories.image_repository import ImageRepository
from src.exceptions import NotFoundError


class GetCommentByIdUseCase:
    def __init__(self, comment_repository: CommentRepository, image_repository: ImageRepository):
        self.comment_repository = comment_repository
        self.image_repository = image_repository

    def execute(self, comment_id: int) -> Comment:
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment", comment_id)
        
        images = self.image_repository.get_by_comment(comment_id)
        
        return Comment(
            id=comment.id,
            text=comment.text,
            post_id=comment.post_id,
            author_id=comment.author_id,
            is_published=comment.is_published,
            created_at=comment.created_at,
            images=[img.url for img in images]
        )
        