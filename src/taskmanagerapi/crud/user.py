from passlib.context import CryptContext
from sqlalchemy.orm import Session
from taskmanagerapi.schemas.user import UserCreate
from taskmanagerapi.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user