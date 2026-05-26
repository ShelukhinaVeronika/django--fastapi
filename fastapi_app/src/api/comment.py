from fastapi import APIRouter, HTTPException, status, Depends, Form, File, UploadFile
from typing import List, Optional
from sqlalchemy import text as sql_text
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.image_repository import ImageRepository
from src.use_cases.comment import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    UpdateCommentUseCase,
)
from src.exceptions import (
    NotFoundError,
    UniqueConstraintError,
    ValidationError,
    NotFoundHTTPError,
    ConflictHTTPError,
    BadRequestHTTPError,
)
from src.api.upload import save_image, delete_image
from src.auth.dependencies import get_current_user
from src.schemas.users import User
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

def get_comment_repository(db: Session = Depends(get_db)):
    return CommentRepository(db)

def get_post_repository(db: Session = Depends(get_db)):
    return PostRepository(db)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_image_repository(db: Session = Depends(get_db)):
    return ImageRepository(db)

@router.get("/", response_model=List[Comment])
def get_all_comments(
    skip: int = 0,
    limit: int = 100,
    post_id: Optional[int] = None,
    only_published: bool = False,
    db: Session = Depends(get_db),
):
    """Получить все комментарии (можно фильтровать по post_id)"""
    comment_repository = get_comment_repository(db)
    image_repository = get_image_repository(db)
    use_case = GetAllCommentsUseCase(comment_repository, image_repository)
    return use_case.execute(skip, limit, post_id, only_published)

@router.get("/{comment_id}", response_model=Comment)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    """Получить комментарий по ID"""
    comment_repository = get_comment_repository(db)
    image_repository = get_image_repository(db)
    use_case = GetCommentByIdUseCase(comment_repository, image_repository)
    try:
        return use_case.execute(comment_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    is_published: bool = Form(True),
    images: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        comment_repository = get_comment_repository(db)
        post_repository = get_post_repository(db)
        user_repository = get_user_repository(db)
        image_repository = get_image_repository(db)

        post = post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundHTTPError("Post", post_id)

        comment_data = CommentCreate(
            text=text,
            post_id=post_id,
            is_published=is_published,
            author_id=current_user.id,
        )

        use_case = CreateCommentUseCase(
            comment_repository, post_repository, user_repository
        )
        comment = use_case.execute(comment_data)

        image_urls = []
        if images:
            for image in images:
                url = save_image(image, current_user.id)
                image_repository.create(url=url, comment_id=comment.id)
                image_urls.append(url)

        comment.images = image_urls
        return comment

    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)
@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    comment_text: Optional[str] = Form(None),
    is_published: Optional[bool] = Form(None),
    images: List[UploadFile] = File(None),
    delete_images: bool = Form(False),  # ← добавить: флаг удаления всех картинок
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить комментарий"""
    from sqlalchemy import text as sql_text
    
    result = db.execute(sql_text("SELECT author_id FROM blog_comment WHERE id = :id"), {"id": comment_id})
    row = result.fetchone()
    if not row:
        raise NotFoundHTTPError("Comment", comment_id)
    if row[0] != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You can only update your own comments")

    if delete_images:
        db.execute(sql_text("DELETE FROM images WHERE comment_id = :comment_id"), {"comment_id": comment_id})
    
    if images:
        for image in images:
            url = save_image(image, current_user.id)
            db.execute(sql_text("INSERT INTO images (url, comment_id) VALUES (:url, :comment_id)"), 
                      {"url": url, "comment_id": comment_id})
    
    if comment_text is not None:
        db.execute(sql_text("UPDATE blog_comment SET text = :text WHERE id = :id"), {"text": comment_text, "id": comment_id})
    if is_published is not None:
        db.execute(sql_text("UPDATE blog_comment SET is_published = :is_published WHERE id = :id"), 
                  {"is_published": is_published, "id": comment_id})
    
    db.commit()

    result = db.execute(sql_text("SELECT id, text, post_id, author_id, is_published, created_at FROM blog_comment WHERE id = :id"), 
                       {"id": comment_id})
    comment_row = result.fetchone()
    
    result = db.execute(sql_text("SELECT url FROM images WHERE comment_id = :comment_id"), {"comment_id": comment_id})
    images_list = [row[0] for row in result.fetchall()]

    return Comment(
        id=comment_row[0],
        text=comment_row[1],
        post_id=comment_row[2],
        author_id=comment_row[3],
        is_published=comment_row[4],
        created_at=comment_row[5],
        images=images_list
    )

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить комментарий"""
    repository = get_comment_repository(db)
    image_repository = get_image_repository(db)

    try:
        existing_comment = repository.get_by_id(comment_id)
        if (
            existing_comment.author_id != current_user.id
            and not current_user.is_superuser
        ):
            raise HTTPException(
                status_code=403, detail="You can only delete your own comments"
            )
        image_repository.delete_by_comment(comment_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)

    use_case = DeleteCommentUseCase(repository)
    try:
        result = use_case.execute(comment_id)
        if not result:
            raise NotFoundHTTPError("Comment", comment_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
