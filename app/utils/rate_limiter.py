from flask import request, abort
from functools import wraps
import time

# Simple in-memory rate limiting
request_counts = {}
RATE_LIMIT = 10  # requests
TIME_WINDOW = 60  # seconds

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        current_time = time.time()
        
        # Clean up old entries
        request_counts.update({
            k: v for k, v in request_counts.items()
            if current_time - v['timestamp'] < TIME_WINDOW
        })
        
        if ip not in request_counts:
            request_counts[ip] = {
                'count': 1,
                'timestamp': current_time
            }
        else:
            if current_time - request_counts[ip]['timestamp'] >= TIME_WINDOW:
                request_counts[ip] = {
                    'count': 1,
                    'timestamp': current_time
                }
            else:
                request_counts[ip]['count'] += 1
                
        if request_counts[ip]['count'] > RATE_LIMIT:
            abort(429, description="Rate limit exceeded")
            
        return f(*args, **kwargs)
    return decorated_function 