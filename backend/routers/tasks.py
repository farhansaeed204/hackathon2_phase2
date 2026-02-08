from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from backend.dependencies import get_current_user
from sqlmodel import Session, select
from backend.database import engine

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskPublic])
def get_tasks(user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks

@router.post("/", response_model=TaskPublic)
def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        db_task = Task.from_orm(task)
        db_task.user_id = user_id
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task_id: str, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@router.put("/{task_id}", response_model=TaskPublic)
def update_task(task_id: str, task_update: TaskUpdate, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(task, key, value)
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@router.delete("/{task_id}")
def delete_task(task_id: str, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle", response_model=TaskPublic)
def toggle_task_completion(task_id: str, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.completed = not task.completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return task