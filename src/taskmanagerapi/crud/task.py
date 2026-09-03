from sqlalchemy.orm import Session
from taskmanagerapi.models.task import Task
from taskmanagerapi.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, owner_id: int, skip: int, limit: int) -> list[Task]:
    tasks = db.query(Task).filter(Task.owner_id == owner_id).order_by(Task.id).offset(skip).limit(limit).all()
    return tasks


def get_task(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def create_task(db: Session, task: TaskCreate, owner_id: int) -> Task:
    db_task = Task(**task.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate, owner_id: int) -> Task | None:
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if db_task is None:
        return None

    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, owner_id: int) -> dict | None:
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}