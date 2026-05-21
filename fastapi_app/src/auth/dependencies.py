from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.jwt import decode_access_token
from src.repositories.user_repository import UserRepository
from src.exceptions import NotFoundError

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    repository = UserRepository("db.sqlite3")
    try:
        user = repository.get_by_id(int(user_id))
        return user
    except NotFoundError:
        raise HTTPException(status_code=401, detail="User not found")