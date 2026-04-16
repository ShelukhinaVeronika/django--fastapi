from typing import Optional
from src.schemas.posts import Post, PostUpdate
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository


class UpdatePostUseCase:
    """Обновить пост"""
    
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
        category_repository: CategoryRepository,
        location_repository: LocationRepository
    ):
        self.post_repository = post_repository
        self.user_repository = user_repository
        self.category_repository = category_repository
        self.location_repository = location_repository
    
    def execute(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        existing_post = self.post_repository.get_by_id(post_id)
        if not existing_post:
            return None
        
        if post_data.category_id:
            category = self.category_repository.get_by_id(post_data.category_id)
            if not category:
                raise ValueError(f"Category with id {post_data.category_id} does not exist")
        
        if post_data.location_id:
            location = self.location_repository.get_by_id(post_data.location_id)
            if not location:
                raise ValueError(f"Location with id {post_data.location_id} does not exist")
        
        updated_post = Post(
            id=post_id,
            title=post_data.title if post_data.title is not None else existing_post.title,
            text=post_data.text if post_data.text is not None else existing_post.text,
            pub_date=post_data.pub_date if post_data.pub_date is not None else existing_post.pub_date,
            author_id=existing_post.author_id,
            location_id=post_data.location_id if post_data.location_id is not None else existing_post.location_id,
            category_id=post_data.category_id if post_data.category_id is not None else existing_post.category_id,
            image=post_data.image if post_data.image is not None else existing_post.image,
            is_published=post_data.is_published if post_data.is_published is not None else existing_post.is_published,
            created_at=existing_post.created_at
        )
        
        return self.post_repository.update(post_id, updated_post)