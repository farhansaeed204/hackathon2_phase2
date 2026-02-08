from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import tasks
from backend.database import create_db_and_tables
import os

app = FastAPI(title="HK2 Phase II Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))