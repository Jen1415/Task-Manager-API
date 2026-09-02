from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from taskmanagerapi.database import get_db
from taskmanagerapi.crud import task as task_crud
from taskmanagerapi.schemas import task as task_schemas

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/tasks",
    tags = ["Tasks"]
)

@router.get("/", response_model=list[task_schemas.TaskResponse])
def get_tasks(db: db_dependency, skip: int = 0, limit: int = 10):
    tasks = task_crud.get_tasks(db, skip, limit)
    return tasks

@router.get("/{task_id}", response_model=task_schemas.TaskResponse)
def get_task(task_id: int, db: db_dependency):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task 

@router.post("/", response_model=task_schemas.TaskResponse)
def create_task(task: task_schemas.TaskCreate, db: db_dependency):
    db_task = task_crud.create_task(db, task, owner_id=1)
    return db_task

@router.patch("/{task_id}", response_model=task_schemas.TaskResponse)
def update_task(task_id: int, task: task_schemas.TaskUpdate, db: db_dependency):
    db_task = task_crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: db_dependency):
    result = task_crud.delete_task(db, task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result