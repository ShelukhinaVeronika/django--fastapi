from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.use_cases.comment import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    UpdateCommentUseCase
)
from src.exceptions import (
    NotFoundError, UniqueConstraintError, ValidationError,
    NotFoundHTTPError, ConflictHTTPError, BadRequestHTTPError
)


router = APIRouter(prefix="/comments", tags=["Comments"])

def get_comment_repository():
    return CommentRepository("db.sqlite3")

def get_post_repository():
    return PostRepository("db.sqlite3")

def get_user_repository():
    return UserRepository("db.sqlite3")


@router.get("/", response_model=List[Comment])
def get_all_comments(
    skip: int = 0, 
    limit: int = 100,
    post_id: Optional[int] = None,
    only_published: bool = False
):
    """Получить все комментарии (можно фильтровать по post_id)"""
    repository = get_comment_repository()
    use_case = GetAllCommentsUseCase(repository)
    return use_case.execute(skip, limit, post_id, only_published)


@router.get("/{comment_id}", response_model=Comment)
def get_comment_by_id(comment_id: int):
    """Получить комментарий по ID"""
    repository = get_comment_repository()
    use_case = GetCommentByIdUseCase(repository)
    try:
        return use_case.execute(comment_id)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment_data: CommentCreate):
    """Создать новый комментарий"""
    comment_repository = get_comment_repository()
    post_repository = get_post_repository()
    user_repository = get_user_repository()
    use_case = CreateCommentUseCase(comment_repository, post_repository, user_repository)
    
    try:
        return use_case.execute(comment_data)
    except UniqueConstraintError as e:
        raise ConflictHTTPError(e.entity_name, e.field, e.value)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)



@router.put("/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, comment_data: CommentUpdate):
    """Обновить комментарий"""
    repository = get_comment_repository()
    use_case = UpdateCommentUseCase(repository)
    
    try:
        return use_case.execute(comment_id, comment_data)
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
    except ValidationError as e:
        raise BadRequestHTTPError(e.message, e.field)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int):
    """Удалить комментарий"""
    repository = get_comment_repository()
    use_case = DeleteCommentUseCase(repository)
    try:
        result = use_case.execute(comment_id)
        if not result:
            raise NotFoundHTTPError("Comment", comment_id)
        return None
    except NotFoundError as e:
        raise NotFoundHTTPError(e.entity_name, e.entity_id)
