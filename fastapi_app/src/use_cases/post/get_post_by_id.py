from typing import Optional, Dict, Any
from src.schemas.posts import Post
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.exceptions import NotFoundError


class GetPostByIdUseCase:
    """Получить пост по ID с комментариями"""

    def __init__(
        self, post_repository: PostRepository, comment_repository: CommentRepository
    ):
        self.post_repository = post_repository
        self.comment_repository = comment_repository

    def execute(
        self, post_id: int, include_comments: bool = True
    ) -> Optional[Dict[str, Any]]:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post", post_id)

        result = {
            "id": post.id,
            "title": post.title,
            "text": post.text,
            "pub_date": post.pub_date,
            "author_id": post.author_id,
            "location_id": post.location_id,
            "category_id": post.category_id,
            "is_published": post.is_published,
            "created_at": post.created_at,
            "images": [img.url for img in post.images] if hasattr(post, 'images') else []
        }

        if include_comments:
            comments = self.comment_repository.get_by_post(post_id)
            result["comments"] = [
                {
                    "id": c.id,
                    "text": c.text,
                    "author_id": c.author_id,
                    "created_at": c.created_at,
                    "is_published": c.is_published,
                    "images": [img.url for img in c.images] if hasattr(c, 'images') else []
                }
                for c in comments
            ]

        return result
