from fastapi import HTTPException, Request
from loguru import logger
import time
from collections import defaultdict, deque

# Rate limit configuration
CALLS_LIMIT = 10  # Number of calls
PERIOD = 60  # Seconds

# Store IP timestamps
request_history = defaultdict(lambda: deque(maxlen=CALLS_LIMIT))

def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        client_ip = x_forwarded_for.split(",")[0]
    else:
        # If no X-Forwarded-For header, use the client's direct IP
        client_ip = request.client.host
    return client_ip

async def rate_limit(request: Request):
    """
    Rate limiting function using client IP.
    Returns True if request is allowed, raises HTTPException if rate limit exceeded.
    """
    client_ip = get_client_ip(request)
    
    current_time = time.time()
    request_times = request_history[client_ip]
    
    # If we have enough requests and the oldest is within our window
    if (len(request_times) >= CALLS_LIMIT and 
        current_time - request_times[0] < PERIOD):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {CALLS_LIMIT} calls per {PERIOD} seconds."
        )
    
    # Add current request time
    request_times.append(current_time)
    logger.debug(f"Request allowed for IP: {client_ip}")
    return True 