from typing import List, Optional
from src.schemas.posts import Post
from src.repositories.post_repository import PostRepository


class GetAllPostsUseCase:
    """Получить все посты"""
    
    def __init__(self, repository: PostRepository):
        self.repository = repository
    
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
            posts = self.repository.get_published_posts()
        elif author_id:
            posts = self.repository.get_by_author(author_id)
        elif category_id:
            posts = self.repository.get_by_category(category_id)
        elif location_id:
            posts = self.repository.get_by_location(location_id)
        else:
            posts = self.repository.get_all()
        
        return posts[skip:skip + limit]