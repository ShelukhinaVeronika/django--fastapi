from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile
from typing import List, Optional
from src.schemas.posts import Post, PostCreate, PostUpdate
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.image_repository import ImageRepository 
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

def get_image_repository(db: Session = Depends(get_db)):
    return ImageRepository(db)

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
    post_repository = get_post_repository(db)
    image_repository = get_image_repository(db)
    use_case = GetAllPostsUseCase(post_repository, image_repository)
    return use_case.execute(skip, limit, author_id, category_id, location_id, only_published)

@router.get("/{post_id}")
def get_post_by_id(
    post_id: int, include_comments: bool = True, db: Session = Depends(get_db)
):
    post_repository = get_post_repository(db)
    comment_repository = get_comment_repository(db)
    image_repository = get_image_repository(db) 
    use_case = GetPostByIdUseCase(post_repository, comment_repository, image_repository)  

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
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый пост с картинкой"""

    try:
        post_repository = get_post_repository(db)
        user_repository = get_user_repository(db)
        category_repository = get_category_repository(db)
        location_repository = get_location_repository(db)
        image_repository = get_image_repository(db)

        image_urls = []
        for image in images:
            url = save_image(image, current_user.id)
            image_urls.append(url)

        post_data = PostCreate(
            title=title,
            text=text,
            location_id=location_id,
            category_id=category_id,
            is_published=is_published,
            author_id=current_user.id,
        )

        use_case = CreatePostUseCase(
            post_repository, user_repository, category_repository, location_repository
        )

        post = use_case.execute(post_data)
    
        for url in image_urls:
            image_repository.create(url=url, post_id=post.id)
    
        post.images = image_urls
    
        return post

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
    images: List[UploadFile] = File(None),
    delete_images: bool = Form(False),  # ← добавить
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить пост с возможностью добавления и удаления картинок"""
    from sqlalchemy import text as sql_text
    
    post_repository = get_post_repository(db)
    user_repository = get_user_repository(db)
    category_repository = get_category_repository(db)
    location_repository = get_location_repository(db)

    try:
        existing_post = post_repository.get_by_id(post_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    
    if existing_post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You can only update your own posts"
        )
    
    if delete_images:
        db.execute(sql_text("DELETE FROM images WHERE post_id = :post_id"), {"post_id": post_id})
    
    if images:
        for image in images:
            url = save_image(image, current_user.id)
            db.execute(sql_text("INSERT INTO images (url, post_id) VALUES (:url, :post_id)"), 
                      {"url": url, "post_id": post_id})
    
    post_data = PostUpdate(
        title=title,
        text=text,
        location_id=location_id,
        category_id=category_id,
        is_published=is_published,
    )

    use_case = UpdatePostUseCase(
        post_repository, user_repository, category_repository, location_repository
    )

    try:
        updated_post = use_case.execute(post_id, post_data)
        
        result = db.execute(sql_text("SELECT url FROM images WHERE post_id = :post_id"), {"post_id": post_id})
        images_list = [row[0] for row in result.fetchall()]
        updated_post.images = images_list
        
        return updated_post
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
    """Удалить пост и все его картинки"""
    post_repository = get_post_repository(db)
    comment_repository = get_comment_repository(db)
    image_repository = get_image_repository(db)

    try:
        existing_post = post_repository.get_by_id(post_id)
        if existing_post.author_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="You can only delete your own posts"
            )
        image_repository.delete_by_post(post_id)
        
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)

    use_case = DeletePostUseCase(post_repository, comment_repository)
    try:
        result = use_case.execute(post_id)
        if not result:
            raise NotFoundHTTPError("Post", post_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
