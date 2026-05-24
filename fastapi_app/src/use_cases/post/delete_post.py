from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.exceptions import NotFoundError


class DeletePostUseCase:
    """Удалить пост"""

    def __init__(
        self, post_repository: PostRepository, comment_repository: CommentRepository
    ):
        self.post_repository = post_repository
        self.comment_repository = comment_repository

    def execute(self, post_id: int) -> bool:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post", post_id)

        comments = self.comment_repository.get_by_post(post_id)
        for comment in comments:
            self.comment_repository.delete(comment.id)

        return self.post_repository.delete(post_id)
