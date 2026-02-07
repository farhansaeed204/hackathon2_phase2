# Task CRUD Skill

## Description
Handles all Create, Read, Update, and Delete operations for tasks in the system.

## Capabilities
- Create new tasks with validation
- Retrieve all tasks for a specific user
- Retrieve a single task by ID
- Update task properties
- Delete tasks
- Toggle task completion status
- Validate user ownership of tasks

## Implementation Notes
- All operations must validate user ID against JWT token
- Proper error handling for all operations
- Consistent response format
- Database transaction management
- Input validation for all operations