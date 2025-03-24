from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger
import os

from app.api.routes import router as api_router

# Configure logger
logger.add("logs/api.log", rotation="10 MB", level="INFO")

app = FastAPI(
    title="YouTube Transcript Downloader API",
    description="API for downloading YouTube video transcripts",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

@app.get("/")
async def root():
    """Serve the frontend HTML page"""
    return FileResponse("app/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 