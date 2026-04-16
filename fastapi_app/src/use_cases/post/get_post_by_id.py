from typing import Optional, Dict, Any
from src.schemas.posts import Post
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository


class GetPostByIdUseCase:
    """Получить пост по ID с комментариями"""
    
    def __init__(self, post_repository: PostRepository, comment_repository: CommentRepository):
        self.post_repository = post_repository
        self.comment_repository = comment_repository
    
    def execute(self, post_id: int, include_comments: bool = True) -> Optional[Dict[str, Any]]:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            return None
        
        result = post.model_dump()
        
        if include_comments:
            comments = self.comment_repository.get_by_post(post_id)
            result['comments'] = [c.model_dump() for c in comments]
        
        return result