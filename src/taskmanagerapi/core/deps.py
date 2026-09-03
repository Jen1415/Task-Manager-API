from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from taskmanagerapi.database import get_db
from taskmanagerapi.core.security import decode_access_token
from taskmanagerapi.crud import user as user_crud
from taskmanagerapi.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
db_dependency = Annotated[Session, Depends(get_db)]

def get_current_user(db: db_dependency, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_access_token(token)

    if token is None:
        raise credentials_exception
    
    email = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = user_crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user