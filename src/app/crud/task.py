import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def list_for_admin(db: Session, user_id: uuid.UUID) -> list[Task]:
    return list(db.execute(select(Task).order_by(Task.title)).scalars())

def list_for_user(db: Session, user_id: uuid.UUID) -> list[Task]:
    return list(db.execute(select(Task).where(Task.user_id == user_id).order_by(Task.title)).scalars())

def get_for_user(db: Session, user_id: uuid.UUID, task_id: uuid.UUID) -> Task | None:
    return db.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id)).scalar_one_or_none()

def create_for_user(db: Session, user_id: uuid.UUID, data: TaskCreate) -> Task:
    
    task = Task(
        user_id=user_id, 
        title=data.title, 
        description=data.description,
        priority=data.priority,
        due_at=data.due_at      
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update(db: Session, task: Task, data: TaskUpdate) -> Task:
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

def delete(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
