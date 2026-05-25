from typing import List, Optional
from src.schemas.comments import Comment
from src.repositories.comment_repository import CommentRepository
from src.repositories.image_repository import ImageRepository


class GetAllCommentsUseCase:
    def __init__(self, comment_repository: CommentRepository, image_repository: ImageRepository):
        self.comment_repository = comment_repository
        self.image_repository = image_repository

    def execute(self, skip: int = 0, limit: int = 100, post_id: Optional[int] = None, only_published: bool = False) -> List[Comment]:
        if post_id:
            comments = self.comment_repository.get_by_post(post_id)
        elif only_published:
            comments = self.comment_repository.get_published()
        else:
            comments = self.comment_repository.get_all()
        
        result = []
        for comment in comments:
            images = self.image_repository.get_by_comment(comment.id)
            result.append(Comment(
                id=comment.id,
                text=comment.text,
                post_id=comment.post_id,
                author_id=comment.author_id,
                is_published=comment.is_published,
                created_at=comment.created_at,
                images=[img.url for img in images]
            ))
        
        return result[skip:skip + limit]
