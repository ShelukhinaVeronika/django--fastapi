from src.repositories.user_repository import UserRepository
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.exceptions import NotFoundError


class DeleteUserUseCase:
    """Удалить пользователя"""
    def __init__(
        self,
        user_repository: UserRepository,
        post_repository: PostRepository,
        comment_repository: CommentRepository
    ):
        self.user_repository = user_repository
        self.post_repository = post_repository
        self.comment_repository = comment_repository
    
    def execute(self, user_id: int) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        comments = self.comment_repository.get_by_author(user_id)
        for comment in comments:
            self.comment_repository.delete(comment.id)
    
        posts = self.post_repository.get_by_author(user_id)
        for post in posts:
            post_comments = self.comment_repository.get_by_post(post.id)
            for comment in post_comments:
                self.comment_repository.delete(comment.id)
            self.post_repository.delete(post.id)
        
        return self.user_repository.delete(user_id)
