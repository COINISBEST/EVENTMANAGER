from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests  # Number of requests allowed
        self.window = window  # Time window in seconds
        self.clients: Dict[str, Tuple[int, float]] = {}  # IP: (requests, start_time)
    
    async def check(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip in self.clients:
            requests, start_time = self.clients[client_ip]
            time_passed = current_time - start_time
            
            if time_passed > self.window:
                # Reset if window has passed
                self.clients[client_ip] = (1, current_time)
            elif requests >= self.requests:
                # Rate limit exceeded
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
            else:
                # Increment request count
                self.clients[client_ip] = (requests + 1, start_time)
        else:
            # First request from this IP
            self.clients[client_ip] = (1, current_time)

# Create rate limiters for different endpoints
email_limiter = RateLimiter(requests=3, window=300)  # 3 requests per 5 minutes
auth_limiter = RateLimiter(requests=5, window=60)    # 5 requests per minute 