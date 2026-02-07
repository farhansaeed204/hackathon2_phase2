from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import TaskService
from src.core.database import get_session
from src.services.auth import get_current_user
from src.core.logging import logger
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(tags=["tasks"])

@router.post("/", response_model=TaskRead)
@limiter.limit("10/minute")  # Limit to 10 task creations per minute per IP
async def create_task(
    request: Request,
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        # Validate input data
        if not task_data.title or len(task_data.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required"
            )

        task_service = TaskService(session)
        task = await task_service.create_task(task_data, user_id)
        logger.info(f"Task created successfully: {task.id} for user: {user_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while creating task"
        )


@router.get("/{task_id}", response_model=TaskRead)
@limiter.limit("20/minute")  # Limit to 20 task retrievals per minute per IP
async def get_task(
    request: Request,
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    try:
        task_service = TaskService(session)
        task = await task_service.get_task_by_id(task_id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Task retrieved successfully: {task_id} for user: {user_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving task"
        )


@router.get("/", response_model=List[TaskRead])
@limiter.limit("20/minute")  # Limit to 20 task list requests per minute per IP
async def get_tasks(
    request: Request,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all tasks for the authenticated user.
    """
    try:
        # Validate parameters
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip parameter must be non-negative"
            )

        if limit <= 0 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit parameter must be between 1 and 1000"
            )

        task_service = TaskService(session)
        tasks = await task_service.get_tasks_by_user(user_id, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving tasks"
        )


@router.put("/{task_id}", response_model=TaskRead)
@limiter.limit("15/minute")  # Limit to 15 task updates per minute per IP
async def update_task(
    request: Request,
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    try:
        # Validate input data
        if task_data.title is not None and (not task_data.title or len(task_data.title.strip()) == 0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )

        task_service = TaskService(session)
        task = await task_service.update_task(task_id, task_data, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Task updated successfully: {task_id} for user: {user_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating task"
        )


@router.delete("/{task_id}")
@limiter.limit("10/minute")  # Limit to 10 task deletions per minute per IP
async def delete_task(
    request: Request,
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    try:
        task_service = TaskService(session)
        success = await task_service.delete_task(task_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Task deleted successfully: {task_id} for user: {user_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while deleting task"
        )


@router.patch("/{task_id}/complete", response_model=TaskRead)
@limiter.limit("15/minute")  # Limit to 15 task completion toggles per minute per IP
async def toggle_task_completion(
    request: Request,
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    """
    try:
        task_service = TaskService(session)
        task = await task_service.toggle_task_completion(task_id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Task completion toggled successfully: {task_id} for user: {user_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling task completion {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while toggling task completion"
        )