import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud import task as crud_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskOut], description="List all tasks belonging to the current user.")
def list_tasks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud_task.list_for_user(db, user.id)

@router.post("", response_model=TaskOut, status_code=201, description="Create a new task for the current user.")
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud_task.create_for_user(db, user.id, payload)

@router.get("/{task_id}", response_model=TaskOut, description="Get a specific task belonging to the current user.")
def get_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = crud_task.get_for_user(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskOut, description="Update a specific task belonging to the current user.")
def update_task(
    task_id: uuid.UUID,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = crud_task.get_for_user(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud_task.update(db, task, payload)

@router.delete("/{task_id}", status_code=204, description="Delete a specific task belonging to the current user.")
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = crud_task.get_for_user(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud_task.delete(db, task)
    return None
