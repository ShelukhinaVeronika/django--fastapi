from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.comment_repository import CommentRepository
from src.use_cases.post import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetAllPostsUseCase,
    GetPostByIdUseCase,
    UpdatePostUseCase
)
from src.exceptions import (
    NotFoundError, UniqueConstraintError, ValidationError,
    NotFoundHTTPError, ConflictHTTPError, BadRequestHTTPError
)


router = APIRouter(prefix="/posts", tags=["Posts"])

def get_post_repository():
    return PostRepository("db.sqlite3")

def get_user_repository():
    return UserRepository("db.sqlite3")

def get_category_repository():
    return CategoryRepository("db.sqlite3")

def get_location_repository():
    return LocationRepository("db.sqlite3")

def get_comment_repository():
    return CommentRepository("db.sqlite3")


@router.get("/", response_model=List[Post])
def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    only_published: bool = False
):
    """Получить все посты с фильтрацией"""
    repository = get_post_repository()
    use_case = GetAllPostsUseCase(repository)
    return use_case.execute(skip, limit, author_id, category_id, location_id, only_published)


@router.get("/{post_id}")
def get_post_by_id(post_id: int, include_comments: bool = True):
    """Получить пост по ID с комментариями"""
    post_repository = get_post_repository()
    comment_repository = get_comment_repository()
    use_case = GetPostByIdUseCase(post_repository, comment_repository)
    
    try:
        return use_case.execute(post_id, include_comments)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate):
    """Создать новый пост"""
    post_repository = get_post_repository()
    user_repository = get_user_repository()
    category_repository = get_category_repository()
    location_repository = get_location_repository()
    
    use_case = CreatePostUseCase(
        post_repository,
        user_repository,
        category_repository,
        location_repository
    )
    
    try:
        return use_case.execute(post_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post_data: PostUpdate):
    """Обновить пост"""
    post_repository = get_post_repository()
    user_repository = get_user_repository()
    category_repository = get_category_repository()
    location_repository = get_location_repository()
    
    use_case = UpdatePostUseCase(
        post_repository,
        user_repository,
        category_repository,
        location_repository
    )
    
    try:
        return use_case.execute(post_id, post_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """Удалить пост"""
    repository = get_post_repository()
    use_case = DeletePostUseCase(repository)
    try:
        result = use_case.execute(post_id)
        if not result:
            raise NotFoundHTTPError("Post", post_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    