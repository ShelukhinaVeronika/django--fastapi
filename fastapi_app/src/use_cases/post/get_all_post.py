from typing import List, Optional
from src.schemas.posts import Post
from src.repositories.post_repository import PostRepository
from src.repositories.image_repository import ImageRepository


class GetAllPostsUseCase:
    def __init__(self, post_repository: PostRepository, image_repository: ImageRepository):
        self.post_repository = post_repository
        self.image_repository = image_repository

    def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None,
        only_published: bool = False
    ) -> List[Post]:
        if only_published:
            posts = self.post_repository.get_published_posts()
        elif author_id:
            posts = self.post_repository.get_by_author(author_id)
        elif category_id:
            posts = self.post_repository.get_by_category(category_id)
        elif location_id:
            posts = self.post_repository.get_by_location(location_id)
        else:
            posts = self.post_repository.get_all()
        
        result = []
        for post in posts:
            images = self.image_repository.get_by_post(post.id)
            result.append(Post(
                id=post.id,
                title=post.title,
                text=post.text,
                pub_date=post.pub_date,
                author_id=post.author_id,
                location_id=post.location_id,
                category_id=post.category_id,
                is_published=post.is_published,
                created_at=post.created_at,
                images=[img.url for img in images]
            ))
        
        return result[skip:skip + limit]
