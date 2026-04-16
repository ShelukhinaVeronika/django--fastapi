from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from src.schemas.comments import Comment, CommentCreate, CommentUpdate
from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository
from src.use_cases.comment import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    UpdateCommentUseCase
)

router = APIRouter(prefix="/comments", tags=["Comments"])

def get_comment_repository():
    return CommentRepository("db.sqlite3")

def get_post_repository():
    return PostRepository("db.sqlite3")


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
    comment = use_case.execute(comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    return comment


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment_data: CommentCreate):
    """Создать новый комментарий"""
    comment_repository = get_comment_repository()
    post_repository = get_post_repository()
    use_case = CreateCommentUseCase(comment_repository, post_repository)
    
    try:
        comment = use_case.execute(comment_data)
        return comment
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, comment_data: CommentUpdate):
    """Обновить комментарий"""
    repository = get_comment_repository()
    use_case = UpdateCommentUseCase(repository)
    
    comment = use_case.execute(comment_id, comment_data)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int):
    """Удалить комментарий"""
    repository = get_comment_repository()
    use_case = DeleteCommentUseCase(repository)
    
    deleted = use_case.execute(comment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    return None