from app.main import app
from flask import Request

def handler(request):
    """Handle requests for Vercel serverless."""
    if isinstance(request, dict):
        # Convert dict to Request object
        request_obj = Request.from_values(
            base_url=request.get('headers', {}).get('host', ''),
            path=request.get('path', ''),
            query_string=request.get('query', ''),
            method=request.get('method', 'GET'),
            headers=request.get('headers', {}),
            data=request.get('body', '')
        )
        return app.handle_request(request_obj)
    return app(request) 