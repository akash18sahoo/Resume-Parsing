import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import resume

# Create directories on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("app/static", exist_ok=True)
    yield

app = FastAPI(
    title="Resume Parser API",
    description="AI-powered Resume Parser using Google Gemini structured output capability.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins for development/testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Register API endpoints
app.include_router(resume.router, prefix="/api/v1", tags=["Resume Parser"])

# Mount static files to serve the frontend (Phase 6)
# html=True serves index.html at root automatically if it exists in app/static/
try:
    app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
except Exception:
    # Fallback if static folder setup is delayed
    pass
