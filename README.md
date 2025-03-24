# YouTube Transcript Downloader

A web application and REST API built with Python and FastAPI that provides a YouTube transcript downloading service.

## Features

- User-friendly web interface for downloading YouTube video transcripts
- REST API for programmatic access to transcripts
- Input validation and error handling
- Rate limiting to prevent abuse
- Comprehensive logging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-transcript-downloader.git
cd youtube-transcript-downloader
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The web interface will be available at `http://localhost:8000`.

## Using the Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a YouTube video URL in the input field
3. Click "Get Transcript" to fetch and display the transcript
4. Use the "Copy Text" button to copy the full transcript to your clipboard

## API Documentation

The API documentation is available at `http://localhost:8000/docs` (Swagger UI).

### Endpoints

#### POST /api/download-transcript

Downloads the transcript from a YouTube video.

**Request Body:**

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "transcript": [
    {
      "text": "Hello, this is the transcript text",
      "start": 0.5,
      "duration": 2.3
    },
    ...
  ]
}
```

**Error Responses:**

- 400 Bad Request: Invalid URL format or transcript unavailable
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Server-side error

## Deployment

For production deployment, consider:

1. Setting up a proper web server (Nginx, Apache)
2. Using a process manager like Gunicorn
3. Configuring HTTPS
4. Setting appropriate CORS settings in app/main.py

## License

MIT 