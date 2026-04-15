from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime


def get_task(db: Session, task_id: int, owner: User) -> Optional[Task]:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task and (task.owner_id == owner.id or owner.role.value == "admin"):
        return task
    return None


def get_tasks(db: Session, owner: User, skip: int = 0, limit: int = 100) -> List[Task]:
    if owner.role.value == "admin":
        return db.query(Task).offset(skip).limit(limit).all()
    else:
        return db.query(Task).filter(Task.owner_id == owner.id).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate, owner: User) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        owner_id=owner.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate, owner: User) -> Optional[Task]:
    db_task = get_task(db, task_id, owner)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    
    if "is_completed" in update_data and update_data["is_completed"]:
        update_data["status"] = "completed"
        update_data["completed_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, owner: User) -> bool:
    db_task = get_task(db, task_id, owner)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True
