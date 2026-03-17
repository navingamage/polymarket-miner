"""
Rate Limiter Utility
Prevents API blocking by controlling request frequency
"""

import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window_seconds):
        """
        Initialize rate limiter
        max_requests: Maximum requests allowed in time_window
        time_window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window_seconds
        self.requests = deque()

    def wait_if_needed(self):
        """Wait if we've hit the rate limit"""
        now = time.time()

        # Remove requests outside the time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()

        # Check if we need to wait
        if len(self.requests) >= self.max_requests:
            # Calculate how long to wait
            oldest_request = self.requests[0]
            wait_time = oldest_request + self.time_window - now

            if wait_time > 0:
                print(f"⏳ Rate limit hit. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)

        # Record this request
        self.requests.append(now)


# Default limits for Polymarket API
POLYMARKET_LIMITER = RateLimiter(
    max_requests=10,           # 10 requests per 60 seconds
    time_window_seconds=60
)

# Default limits for OpenRouter API
OPENROUTER_LIMITER = RateLimiter(
    max_requests=30,           # 30 requests per 60 seconds
    time_window_seconds=60
)