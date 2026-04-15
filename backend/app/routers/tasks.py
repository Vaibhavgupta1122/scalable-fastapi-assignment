from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task import get_task, get_tasks, create_task, update_task, delete_task
from app.core.security import get_current_active_user, require_user_or_admin

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def get_tasks_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):
    tasks = get_tasks(db, owner=current_user, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    current_user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):
    return create_task(db=db, task=task, owner=current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    current_user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id=task_id, owner=current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_by_id(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):
    task = update_task(db, task_id=task_id, task_update=task_update, owner=current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id(
    task_id: int,
    current_user: User = Depends(require_user_or_admin),
    db: Session = Depends(get_db)
):
    success = delete_task(db, task_id=task_id, owner=current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
