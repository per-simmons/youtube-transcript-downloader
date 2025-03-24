import re
import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from a URL.
    
    Args:
        url: YouTube video URL
        
    Returns:
        str: The YouTube video ID
        
    Raises:
        ValueError: If the video ID cannot be extracted from the URL
    """
    # Try to extract video ID using regex
    patterns = [
        r'(?:v=|/v/|youtu\.be/|/embed/)([^&?/]+)',
        r'youtube\.com/watch\?v=([^&?/]+)',
        r'youtu\.be/([^&?/]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL format")

def get_video_metadata(video_id: str) -> dict:
    """
    Get metadata about a YouTube video (title, channel name).
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        dict: Dictionary containing video metadata
        
    Raises:
        ValueError: If metadata cannot be retrieved
    """
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to get title from meta tags
        title = "Unknown Title"
        title_meta = soup.find("meta", property="og:title")
        if title_meta and title_meta.get("content"):
            title = title_meta["content"]
        
        # Try to get channel name from meta tags
        channel = "Unknown Channel"
        channel_meta = soup.find("link", itemprop="name")
        if channel_meta and channel_meta.get("content"):
            channel = channel_meta["content"]
        
        logger.info(f"Retrieved metadata for video {video_id}: title='{title}', channel='{channel}'")
        
        return {
            "title": title,
            "channel": channel
        }
    except Exception as e:
        logger.error(f"Error fetching video metadata: {str(e)}")
        return {
            "title": "Unknown Title",
            "channel": "Unknown Channel"
        }

def get_transcript(url: str) -> dict:
    """
    Get the transcript for a YouTube video.
    
    Args:
        url: YouTube video URL
        
    Returns:
        dict: A dictionary containing transcript entries and metadata
        
    Raises:
        ValueError: If transcript retrieval fails
    """
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        logger.info(f"Extracting transcript for video ID: {video_id}")
        
        # Get video metadata
        metadata = get_video_metadata(video_id)
        
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format transcript with timestamps
        formatted_lines = []
        for entry in transcript:
            timestamp = int(entry['start'])
            minutes = timestamp // 60
            seconds = timestamp % 60
            text = entry['text'].replace('\n', ' ')
            formatted_lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")
        
        formatted_transcript = '\n'.join(formatted_lines)
        
        logger.info(f"Successfully retrieved transcript for video ID: {video_id}")
        return {
            "transcript": formatted_transcript,
            "metadata": metadata
        }
        
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.error(f"No transcript available for video: {e}")
        raise ValueError(f"No transcript available for this video: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error processing transcript: {str(e)}")
        raise ValueError(f"Failed to process transcript: {str(e)}") 