from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from taskmanagerapi.database import get_db
from taskmanagerapi.crud import user as user_crud
from taskmanagerapi.core.security import create_access_token
from taskmanagerapi.crud.user import pwd_context
from taskmanagerapi.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/login", response_model=Token)
def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.get_user_by_email(db, form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)