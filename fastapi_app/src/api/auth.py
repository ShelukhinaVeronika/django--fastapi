from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.user_repository import UserRepository
from src.auth.hashing import verify_password
from src.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository("db.sqlite3")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    repository = UserRepository("db.sqlite3")

    user = repository.get_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}
