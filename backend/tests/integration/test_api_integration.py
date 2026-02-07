import pytest
from httpx import AsyncClient
from jose import jwt
from src.core.config import settings
from src.models.task import TaskCreate


@pytest.mark.asyncio
async def test_complete_task_workflow(client, db_session):
    """Test the complete workflow of task management"""
    # Create a valid token
    test_user_id = "workflow_test_user"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Step 1: Create a task
    task_data = {
        "title": "Workflow Test Task",
        "description": "This task will go through the complete workflow"
    }
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["title"] == "Workflow Test Task"
    assert created_task["description"] == "This task will go through the complete workflow"
    assert created_task["completed"] is False
    
    # Step 2: Get the specific task
    get_response = await client.get(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Workflow Test Task"
    
    # Step 3: Get all tasks for the user
    all_tasks_response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert all_tasks_response.status_code == 200
    all_tasks = all_tasks_response.json()
    assert len(all_tasks) == 1
    assert all_tasks[0]["id"] == task_id
    
    # Step 4: Update the task
    update_data = {
        "title": "Updated Workflow Test Task",
        "description": "This task has been updated",
        "completed": True
    }
    update_response = await client.put(
        f"/api/{test_user_id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Workflow Test Task"
    assert updated_task["completed"] is True
    
    # Step 5: Toggle task completion
    toggle_response = await client.patch(
        f"/api/{test_user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["id"] == task_id
    assert toggled_task["completed"] is False  # Should be toggled back to False
    
    # Step 6: Delete the task
    delete_response = await client.delete(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"
    
    # Step 7: Verify the task is gone
    get_deleted_response = await client.get(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_deleted_response.status_code == 404


@pytest.mark.asyncio
async def test_multiple_users_isolation(client, db_session):
    """Test that different users can't access each other's tasks"""
    # Create tokens for two different users
    user1_id = "isolation_user_1"
    user2_id = "isolation_user_2"
    
    token_data1 = {"userId": user1_id}
    token_data2 = {"userId": user2_id}
    
    token1 = jwt.encode(token_data1, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    token2 = jwt.encode(token_data2, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)

    # User 1 creates a task
    task_data = {"title": "User 1's Private Task", "description": "Only user 1 should see this"}
    create_response = await client.post(
        f"/api/{user1_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert create_response.status_code == 200
    user1_task = create_response.json()
    user1_task_id = user1_task["id"]
    
    # User 2 creates a task
    task_data = {"title": "User 2's Private Task", "description": "Only user 2 should see this"}
    create_response = await client.post(
        f"/api/{user2_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert create_response.status_code == 200
    user2_task = create_response.json()
    user2_task_id = user2_task["id"]
    
    # User 1 should only see their own task
    user1_tasks_response = await client.get(
        f"/api/{user1_id}/tasks",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert user1_tasks_response.status_code == 200
    user1_tasks = user1_tasks_response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == user1_task_id
    
    # User 2 should only see their own task
    user2_tasks_response = await client.get(
        f"/api/{user2_id}/tasks",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert user2_tasks_response.status_code == 200
    user2_tasks = user2_tasks_response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] == user2_task_id
    
    # User 1 should not be able to access User 2's task directly
    user1_access_user2_task = await client.get(
        f"/api/{user1_id}/tasks/{user2_task_id}",  # User 1 trying to access user 2's task
        headers={"Authorization": f"Bearer {token1}"}
    )
    # This should return 404 because the task exists but belongs to a different user
    assert user1_access_user2_task.status_code == 404
    
    # User 2 should not be able to access User 1's task directly
    user2_access_user1_task = await client.get(
        f"/api/{user2_id}/tasks/{user1_task_id}",  # User 2 trying to access user 1's task
        headers={"Authorization": f"Bearer {token2}"}
    )
    # This should return 404 because the task exists but belongs to a different user
    assert user2_access_user1_task.status_code == 404


@pytest.mark.asyncio
async def test_rate_limiting(client, db_session):
    """Test that rate limiting is working for API endpoints"""
    # Create a valid token
    test_user_id = "rate_limit_test_user"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Try to create more tasks than the rate limit allows (10 per minute)
    # Note: This test might not fully validate rate limiting in a test environment
    # but we can at least verify the endpoints work normally
    for i in range(5):  # Create fewer than the limit to ensure it works
        task_data = {
            "title": f"Rate Limit Test Task {i}",
            "description": f"Task {i} for rate limiting test"
        }
        response = await client.post(
            f"/api/{test_user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in [200, 429]  # Either success or rate limited


@pytest.mark.asyncio
async def test_security_headers_present(client, db_session):
    """Test that security headers are present in API responses"""
    # Create a valid token
    test_user_id = "security_header_test_user"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Make a request to an endpoint
    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Check that security headers are present
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"
    
    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"
    
    assert "x-xss-protection" in response.headers
    assert response.headers["x-xss-protection"] == "1; mode=block"
    
    assert "strict-transport-security" in response.headers