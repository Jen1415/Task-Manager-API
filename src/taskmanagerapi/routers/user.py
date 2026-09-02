from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from taskmanagerapi.database import get_db
from taskmanagerapi.schemas import user as user_schemas
from taskmanagerapi.crud import user as user_crud

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: db_dependency):
    db_user = user_crud.create_user(db, user)
    return db_user