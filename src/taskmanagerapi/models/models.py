import enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from taskmanagerapi.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    suspended = "suspended"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.todo, nullable=False)
    due_date = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)