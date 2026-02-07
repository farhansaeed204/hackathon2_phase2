# Hackathon II Phase II - Task Management System

This is a full-stack task management application built with Next.js frontend and FastAPI backend, featuring JWT authentication and Neon Postgres database.

## Features

- User authentication (login/signup)
- Task management (create, read, update, delete, toggle completion)
- JWT-based authentication
- Responsive UI with Tailwind CSS
- Neon Postgres database integration

## Tech Stack

- Frontend: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, SQLModel, Neon Postgres
- Authentication: JWT tokens
- Deployment: Vercel (frontend), Render (backend)

## Installation

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with your environment variables:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

4. Run the development server:
```bash
npm run dev
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your environment variables:
```env
NEON_DB_URL=your_neon_postgres_database_url
BETTER_AUTH_SECRET=your_jwt_secret_key
```

5. Run the server:
```bash
python start_server.py
```

## Deployment

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Import your project in the Vercel dashboard
3. Configure the build settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Add environment variables in the Vercel dashboard
5. Deploy your project

### Backend Deployment (Render)

1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Set the build command to `pip install -r requirements.txt`
5. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in the Render dashboard:
   - `NEON_DB_URL`
   - `BETTER_AUTH_SECRET`
7. Deploy your service

## API Endpoints

All API endpoints follow the pattern: `/api/users/{user_id}/tasks/`

- `GET /api/users/{user_id}/tasks/` - Get all tasks for a user
- `POST /api/users/{user_id}/tasks/` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a specific task
- `PATCH /api/users/{user_id}/tasks/{task_id}/toggle_complete` - Toggle task completion status

All endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <token>`

## Environment Variables

### Frontend
- `NEXT_PUBLIC_BETTER_AUTH_URL` - The URL of your frontend application

### Backend
- `NEON_DB_URL` - Your Neon Postgres database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT token signing