# HK2 Phase II

This is the Phase II implementation of the Hackathon project, featuring a complete backend API with authentication and a frontend interface.

## Features

- User authentication with JWT
- Task management system
- Responsive UI with Next.js
- NeonDB for data persistence
- FastAPI backend with SQLModel

## Local Development

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the backend:
```bash
cd backend
python main.py
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## Deployment

### Backend Deployment

The backend can be deployed to any cloud provider that supports Docker containers. Here's an example Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python", "main.py"]
```

### Frontend Deployment

The frontend is configured for deployment on Vercel. Simply connect your repository to Vercel and it will automatically build and deploy.

## API Endpoints

- `GET /api/tasks/` - Get all tasks for the authenticated user
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status
- `GET /health` - Health check endpoint

## Environment Variables

### Backend
- `NEON_DB_URL` - Connection string for NeonDB
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins for CORS

### Frontend
- `NEXT_PUBLIC_API_URL` - Base URL for the backend API