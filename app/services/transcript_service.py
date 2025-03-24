import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from loguru import logger
import requests
from bs4 import BeautifulSoup

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
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # youtube.com/watch?v=VIDEO_ID
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',  # youtu.be/VIDEO_ID
        r'(?:embed\/)([0-9A-Za-z_-]{11})',  # youtube.com/embed/VIDEO_ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Could not extract YouTube video ID from the provided URL")

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
        
        if response.status_code != 200:
            logger.warning(f"Failed to get YouTube page for video {video_id}: {response.status_code}")
            return {"title": "", "channel": "", "url": url}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize variables
        title = ""
        channel = ""
        
        # Try to extract title and channel with different methods
        # Method 1: Meta tags
        meta_title = soup.find("meta", property="og:title")
        if meta_title:
            title = meta_title.get("content", "")
        
        # Method 2: Looking for specific channel elements in HTML
        # Try different patterns YouTube might use for channel name
        
        # Look for JSON data in script tags that might contain channel info
        scripts = soup.find_all('script')
        for script in scripts:
            script_text = script.string
            if script_text and '"ownerChannelName":"' in script_text:
                channel_match = re.search(r'"ownerChannelName":"([^"]+)"', script_text)
                if channel_match:
                    channel = channel_match.group(1)
                    break
        
        # If still no channel, look for other common elements
        if not channel:
            # Try to find the channel link and get its text
            channel_link = soup.select_one('a.yt-simple-endpoint.style-scope.yt-formatted-string')
            if channel_link:
                channel = channel_link.text.strip()
        
        # Fallback to any pattern that might indicate channel
        if not channel:
            owner_text = re.search(r'"ownerChannelName":"([^"]+)"', response.text)
            if owner_text:
                channel = owner_text.group(1)
        
        # Final fallback - default to YouTube
        if not channel:
            channel = "Unknown Channel"
            
        # Clean up title
        if " - YouTube" in title:
            title = title.replace(" - YouTube", "")
            
        logger.info(f"Retrieved metadata for video {video_id}: title='{title}', channel='{channel}'")
        
        return {
            "title": title,
            "channel": channel,
            "url": url
        }
        
    except Exception as e:
        logger.error(f"Error fetching video metadata: {e}")
        return {"title": "", "channel": "Unknown Channel", "url": f"https://www.youtube.com/watch?v={video_id}"}

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
        logger.info(f"Extracted video ID: {video_id} from URL: {url}")
        
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Get video metadata
        metadata = get_video_metadata(video_id)
        
        # Process transcript into a more usable format if needed
        processed_transcript = []
        for entry in transcript:
            processed_transcript.append({
                "text": entry.get("text", ""),
                "start": entry.get("start", 0),
                "duration": entry.get("duration", 0)
            })
        
        logger.info(f"Successfully retrieved transcript for video ID: {video_id}")
        return {
            "transcript": processed_transcript,
            "metadata": metadata
        }
        
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.error(f"No transcript available for video: {e}")
        raise ValueError(f"No transcript available for this video: {str(e)}")
    
    except Exception as e:
        logger.error(f"Failed to get transcript: {e}")
        raise ValueError(f"Failed to retrieve transcript: {str(e)}") 