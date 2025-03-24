from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, validator
from loguru import logger
from app.services.transcript_service import get_transcript
from app.utils.rate_limiter import rate_limit
import re

router = APIRouter()

class TranscriptRequest(BaseModel):
    url: str
    
    @validator('url')
    def validate_youtube_url(cls, v):
        # Simple validation for YouTube URL format
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
        if not re.match(youtube_regex, v):
            raise ValueError("Invalid YouTube URL format")
        return v

class ErrorResponse(BaseModel):
    error: str
    details: str = None

@router.post("/download-transcript", 
            summary="Download YouTube transcript",
            response_description="Returns the transcript of the YouTube video")
async def download_transcript(request: Request, transcript_req: TranscriptRequest, limit_check=Depends(rate_limit)):
    """
    Download a transcript from a YouTube video.
    
    - **url**: URL of the YouTube video
    
    Returns the transcript with timestamp information and video metadata.
    """
    try:
        logger.info(f"Transcript download requested for: {transcript_req.url}")
        
        # Extract video ID and get transcript with metadata
        result = get_transcript(transcript_req.url)
        
        return {
            "url": transcript_req.url,
            "transcript": result["transcript"],
            "metadata": result["metadata"]
        }
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error processing transcript request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transcript: {str(e)}"
        ) 