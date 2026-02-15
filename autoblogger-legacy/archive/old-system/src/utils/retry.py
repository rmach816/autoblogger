"""
Retry utilities for AutoBlogger.

Provides exponential backoff retry decorators for handling
API failures, rate limits, and network issues.
"""

import asyncio
import random
from functools import wraps
from typing import Callable, Type, Tuple, Any
from datetime import datetime, timedelta

from models import APIError, RateLimitError, NetworkError
from utils.logger import get_logger

logger = get_logger(__name__)


def retry(
    max_attempts: int = 3,
    backoff_base: float = 2.0,
    backoff_max: float = 60.0,
    jitter: bool = True,
    on_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        backoff_base: Base for exponential backoff calculation
        backoff_max: Maximum backoff time in seconds
        jitter: Add random jitter to prevent thundering herd
        on_exceptions: Tuple of exception types to retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except on_exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
                        raise e
                    
                    # Calculate backoff time
                    backoff_time = min(backoff_base ** attempt, backoff_max)
                    if jitter:
                        backoff_time += random.uniform(0, backoff_time * 0.1)
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {backoff_time:.2f}s"
                    )
                    
                    await asyncio.sleep(backoff_time)
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except on_exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
                        raise e
                    
                    # Calculate backoff time
                    backoff_time = min(backoff_base ** attempt, backoff_max)
                    if jitter:
                        backoff_time += random.uniform(0, backoff_time * 0.1)
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {backoff_time:.2f}s"
                    )
                    
                    import time
                    time.sleep(backoff_time)
            
            raise last_exception
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        async with self._lock:
            now = datetime.now()
            
            # Remove old requests outside the time window
            cutoff = now - timedelta(seconds=self.time_window)
            self.requests = [req_time for req_time in self.requests if req_time > cutoff]
            
            # Check if we can make a request
            if len(self.requests) >= self.max_requests:
                # Calculate wait time
                oldest_request = min(self.requests)
                wait_time = (oldest_request + timedelta(seconds=self.time_window) - now).total_seconds()
                
                if wait_time > 0:
                    logger.info(f"Rate limit reached. Waiting {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)
                    
                    # Clean up again after waiting
                    now = datetime.now()
                    cutoff = now - timedelta(seconds=self.time_window)
                    self.requests = [req_time for req_time in self.requests if req_time > cutoff]
            
            # Record this request
            self.requests.append(now)
    
    def can_make_request(self) -> bool:
        """Check if a request can be made without waiting."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        recent_requests = [req_time for req_time in self.requests if req_time > cutoff]
        return len(recent_requests) < self.max_requests


# Pre-configured rate limiters for common APIs
GEMINI_RATE_LIMITER = RateLimiter(max_requests=15, time_window=60)  # 15 req/min
UNSPLASH_RATE_LIMITER = RateLimiter(max_requests=50, time_window=3600)  # 50 req/hour
GROQ_RATE_LIMITER = RateLimiter(max_requests=30, time_window=60)  # 30 req/min (estimated)


def get_rate_limiter(provider: str) -> RateLimiter:
    """
    Get rate limiter for a specific provider.
    
    Args:
        provider: API provider name
        
    Returns:
        RateLimiter instance for the provider
    """
    limiters = {
        "gemini": GEMINI_RATE_LIMITER,
        "unsplash": UNSPLASH_RATE_LIMITER,
        "groq": GROQ_RATE_LIMITER,
    }
    
    return limiters.get(provider, RateLimiter(max_requests=10, time_window=60))
