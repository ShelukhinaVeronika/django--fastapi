from src.schemas.posts import Post, PostCreate
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository


class CreatePostUseCase:
    """Создать новый пост"""
    
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
    
    def execute(self, post_data: PostCreate) -> Post:
        author = self.user_repository.get_by_id(post_data.author_id)
        if not author:
            raise ValueError(f"User with id {post_data.author_id} does not exist")
        
        if post_data.category_id:
            category = self.category_repository.get_by_id(post_data.category_id)
            if not category:
                raise ValueError(f"Category with id {post_data.category_id} does not exist")
        
        if post_data.location_id:
            location = self.location_repository.get_by_id(post_data.location_id)
            if not location:
                raise ValueError(f"Location with id {post_data.location_id} does not exist")
        
        new_post = Post(
            title=post_data.title,
            text=post_data.text,
            pub_date=post_data.pub_date,
            author_id=post_data.author_id,
            location_id=post_data.location_id,
            category_id=post_data.category_id,
            image=post_data.image,
            is_published=post_data.is_published,
            created_at=post_data.created_at
        )
        
        return self.post_repository.create(new_post)