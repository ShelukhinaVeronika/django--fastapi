from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.jwt import decode_access_token
from src.repositories.user_repository import UserRepository
from src.exceptions import NotFoundError
from src.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    repository = UserRepository("db.sqlite3")
    user = repository.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user