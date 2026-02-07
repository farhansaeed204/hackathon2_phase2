# Data Model

## Task Entity

### Fields
- **id** (UUID/Integer): Primary key, unique identifier for each task
- **user_id** (String/UUID): Foreign key linking task to user, required for data isolation
- **title** (String): Task title, required field with max length validation
- **description** (String): Optional task description, nullable
- **completed** (Boolean): Task completion status, default false
- **created_at** (DateTime): Timestamp when task was created, auto-generated
- **updated_at** (DateTime): Timestamp when task was last updated, auto-generated

### Relationships
- **User**: Many-to-one relationship (many tasks belong to one user)
- **Indexes**: Index on user_id for efficient filtering by authenticated user

### Validation Rules
- Title is required and must be between 1-255 characters
- Description, if provided, must be under 1000 characters
- user_id must correspond to an existing user record
- completed field must be a boolean value

### State Transitions
- New task: completed = false by default
- Task completion: completed = true when toggled
- Task reopening: completed = false when toggled back

## User Entity (Referenced)

### Fields (from Better Auth)
- **id** (UUID/String): Unique user identifier
- **email** (String): User's email address
- **created_at** (DateTime): Account creation timestamp

### Relationships
- **Tasks**: One-to-many relationship (one user has many tasks)