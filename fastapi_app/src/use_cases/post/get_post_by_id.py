from typing import Dict, Any
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.image_repository import ImageRepository
from src.exceptions import NotFoundError


class GetPostByIdUseCase:
    def __init__(self, post_repository: PostRepository, comment_repository: CommentRepository, image_repository: ImageRepository):
        self.post_repository = post_repository
        self.comment_repository = comment_repository
        self.image_repository = image_repository

    def execute(self, post_id: int, include_comments: bool = True) -> Dict[str, Any]:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post", post_id)
        
        post_images = self.image_repository.get_by_post(post_id)
        
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
            "images": [img.url for img in post_images]
        }

        if include_comments:
            comments = self.comment_repository.get_by_post(post_id)
            result["comments"] = []
            for comment in comments:
                comment_images = self.image_repository.get_by_comment(comment.id)
                result["comments"].append({
                    "id": comment.id,
                    "text": comment.text,
                    "author_id": comment.author_id,
                    "created_at": comment.created_at,
                    "is_published": comment.is_published,
                    "images": [img.url for img in comment_images]
                })

        return result