import pytest
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from uuid import uuid4


def test_task_creation():
    """Test creating a Task instance"""
    user_id = str(uuid4())
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "user_id": user_id
    }
    
    task = Task(**task_data)
    
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.completed is False
    assert task.user_id == user_id
    assert task.id is not None  # Should be auto-generated


def test_task_create_model():
    """Test the TaskCreate model validation"""
    user_id = str(uuid4())
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "user_id": user_id
    }
    
    task_create = TaskCreate(**task_data)
    
    assert task_create.title == "Test Task"
    assert task_create.description == "This is a test task"
    assert task_create.completed is False
    assert task_create.user_id == user_id


def test_task_update_model():
    """Test the TaskUpdate model with partial updates"""
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    
    task_update = TaskUpdate(**update_data)
    
    assert task_update.title == "Updated Task"
    assert task_update.completed is True
    assert task_update.description is None  # Should be optional


def test_task_read_model():
    """Test the TaskRead model"""
    user_id = str(uuid4())
    task_data = {
        "id": str(uuid4()),
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    task_read = TaskRead(**task_data)
    
    assert task_read.id == task_data["id"]
    assert task_read.title == "Test Task"
    assert task_read.description == "This is a test task"
    assert task_read.completed is False
    assert task_read.created_at == task_data["created_at"]
    assert task_read.updated_at == task_data["updated_at"]


def test_task_title_validation():
    """Test that Task model enforces title length constraints"""
    user_id = str(uuid4())
    
    # Test that empty title fails validation
    with pytest.raises(ValueError):
        Task(title="", description="Test desc", user_id=user_id)
    
    # Test that very long title fails validation
    with pytest.raises(ValueError):
        long_title = "t" * 256  # Exceeds max length of 255
        Task(title=long_title, description="Test desc", user_id=user_id)
    
    # Test that valid title passes validation
    valid_title = "t" * 255  # At max length
    task = Task(title=valid_title, description="Test desc", user_id=user_id)
    assert task.title == valid_title


def test_task_description_length_validation():
    """Test that Task model enforces description length constraints"""
    user_id = str(uuid4())
    
    # Test that very long description fails validation
    long_desc = "d" * 1001  # Exceeds max length of 1000
    with pytest.raises(ValueError):
        Task(title="Test", description=long_desc, user_id=user_id)
    
    # Test that valid description passes validation
    valid_desc = "d" * 1000  # At max length
    task = Task(title="Test", description=valid_desc, user_id=user_id)
    assert task.description == valid_desc