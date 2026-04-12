from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, submit, task, progress

from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.PROJECT_NAME)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(submit.router, prefix="/submit", tags=["Submission"])
app.include_router(task.router, prefix="/task", tags=["Task"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])

@app.get("/")
async def root():
    return {"message": "Welcome to SpeakBetter API"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
