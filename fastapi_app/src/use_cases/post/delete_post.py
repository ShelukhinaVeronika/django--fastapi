from src.repositories.post_repository import PostRepository


class DeletePostUseCase:
    """Удалить пост"""
    
    def __init__(self, repository: PostRepository):
        self.repository = repository
    
    def execute(self, post_id: int) -> bool:
        return self.repository.delete(post_id)