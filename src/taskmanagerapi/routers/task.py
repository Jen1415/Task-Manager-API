from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from taskmanagerapi.database import get_db
from taskmanagerapi.crud import task as task_crud
from taskmanagerapi.schemas import task as task_schemas
from taskmanagerapi.models.user import User
from taskmanagerapi.core.deps import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]

current_user_dependency = Annotated[User, Depends(get_current_user)]

router = APIRouter(
    prefix="/tasks",
    tags = ["Tasks"]
)

@router.get("/", response_model=list[task_schemas.TaskResponse])
def get_tasks(db: db_dependency, current_user: current_user_dependency, skip: int = 0, limit: int = 10,):
    tasks = task_crud.get_tasks(db, current_user.id, skip, limit)
    return tasks

@router.get("/{task_id}", response_model=task_schemas.TaskResponse)
def get_task(task_id: int, db: db_dependency, current_user: current_user_dependency):
    db_task = task_crud.get_task(db, task_id, current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task 

@router.post("/", response_model=task_schemas.TaskResponse)
def create_task(task: task_schemas.TaskCreate, db: db_dependency, current_user: current_user_dependency):
    db_task = task_crud.create_task(db, task, owner_id=current_user.id)
    return db_task

@router.patch("/{task_id}", response_model=task_schemas.TaskResponse)
def update_task(task_id: int, task: task_schemas.TaskUpdate, db: db_dependency, current_user: current_user_dependency):
    db_task = task_crud.update_task(db, task_id, task, current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: db_dependency, current_user: current_user_dependency):
    result = task_crud.delete_task(db, task_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result