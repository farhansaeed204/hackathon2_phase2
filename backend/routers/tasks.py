from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import select
from typing import List
from ..database import get_async_session
from ..models.task import Task, TaskResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ..dependencies import verify_user_id

router = APIRouter()


@router.get("/{user_id}/tasks/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        statement = select(Task).where(Task.user_id == verified_user_id)
        result = await session.execute(statement)
        tasks = result.scalars().all()
        
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            ) for task in tasks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.post("/{user_id}/tasks/", response_model=TaskResponse)
async def create_task(
    user_id: int,
    task_data: Task,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        # Verify that the user_id in the task matches the authenticated user
        if task_data.user_id != verified_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create task for this user"
            )
        
        # Create new task
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=verified_user_id
        )
        
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        
        return TaskResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            user_id=db_task.user_id,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data provided"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: int,
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == verified_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: int,
    task_id: int,
    task_data: Task,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == verified_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update task fields
        task.title = task_data.title
        task.description = task_data.description
        task.completed = task_data.completed
        task.updated_at = datetime.utcnow()
        
        await session.commit()
        await session.refresh(task)
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data provided"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: int,
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == verified_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        await session.delete(task)
        await session.commit()
        
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


@router.patch("/{user_id}/tasks/{task_id}/toggle_complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: int,
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task by ID for a specific user
    """
    # Verify user ID
    verified_user_id = await verify_user_id(user_id, request)
    
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == verified_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        
        await session.commit()
        await session.refresh(task)
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling task completion: {str(e)}"
        )