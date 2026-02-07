from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models.task import Task

# Create tables
Task.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-production-url.com"],  # Add your production URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from .routers import tasks
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Task API is running!"}