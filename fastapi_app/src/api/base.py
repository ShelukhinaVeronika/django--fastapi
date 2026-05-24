from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile
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
    UpdatePostUseCase,
)
from src.exceptions import (
    NotFoundError,
    UniqueConstraintError,
    ValidationError,
    NotFoundHTTPError,
    ConflictHTTPError,
    BadRequestHTTPError,
)
from src.auth.dependencies import get_current_user
from src.schemas.users import User
from src.api.upload import save_image, delete_image
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_post_repository(db: Session = Depends(get_db)):
    return PostRepository(db)


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_category_repository(db: Session = Depends(get_db)):
    return CategoryRepository(db)


def get_location_repository(db: Session = Depends(get_db)):
    return LocationRepository(db)


def get_comment_repository(db: Session = Depends(get_db)):
    return CommentRepository(db)


@router.get("/", response_model=List[Post])
def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    only_published: bool = False,
    db: Session = Depends(get_db),
):
    """Получить все посты с фильтрацией"""
    repository = get_post_repository(db)
    use_case = GetAllPostsUseCase(repository)
    return use_case.execute(
        skip, limit, author_id, category_id, location_id, only_published
    )


@router.get("/{post_id}")
def get_post_by_id(
    post_id: int, include_comments: bool = True, db: Session = Depends(get_db)
):
    """Получить пост по ID с комментариями"""
    post_repository = get_post_repository(db)
    comment_repository = get_comment_repository(db)
    use_case = GetPostByIdUseCase(post_repository, comment_repository)

    try:
        return use_case.execute(post_id, include_comments)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    title: str = Form(...),
    text: str = Form(...),
    location_id: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
    is_published: bool = Form(True),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый пост с картинкой"""
    post_repository = get_post_repository(db)
    user_repository = get_user_repository(db)
    category_repository = get_category_repository(db)
    location_repository = get_location_repository(db)

    image_url = None
    if image:
        image_url = save_image(image, current_user.id)

    post_data = PostCreate(
        title=title,
        text=text,
        location_id=location_id,
        category_id=category_id,
        is_published=is_published,
        image=image_url,
        author_id=current_user.id,
    )

    use_case = CreatePostUseCase(
        post_repository, user_repository, category_repository, location_repository
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
def update_post(
    post_id: int,
    title: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    location_id: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
    is_published: Optional[bool] = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить пост с возможностью смены картинки"""
    post_repository = get_post_repository(db)
    user_repository = get_user_repository(db)
    category_repository = get_category_repository(db)
    location_repository = get_location_repository(db)

    try:
        existing_post = post_repository.get_by_id(post_id)
        if existing_post.author_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="You can only update your own posts"
            )
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)

    image_url = existing_post.image
    if image:
        if existing_post.image:
            delete_image(existing_post.image)
        image_url = save_image(image, current_user.id)

    post_data = PostUpdate(
        title=title,
        text=text,
        location_id=location_id,
        category_id=category_id,
        is_published=is_published,
        image=image_url,
    )

    use_case = UpdatePostUseCase(
        post_repository, user_repository, category_repository, location_repository
    )

    try:
        return use_case.execute(post_id, post_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить пост и его картинку"""
    repository = get_post_repository(db)

    try:
        existing_post = repository.get_by_id(post_id)
        if existing_post.author_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="You can only delete your own posts"
            )

        if existing_post.image:
            delete_image(existing_post.image)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)

    use_case = DeletePostUseCase(repository)
    try:
        result = use_case.execute(post_id)
        if not result:
            raise NotFoundHTTPError("Post", post_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
