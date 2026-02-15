"""
Rate limiting utilities for API protection.

Provides decorators and utilities for limiting request rates
to prevent abuse and ensure fair usage.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable
from functools import wraps
from collections import defaultdict

from utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter for API requests.
    
    Implements a token bucket algorithm with configurable capacity
    and refill rate.
    """
    
    def __init__(self, capacity: int, refill_rate: float, refill_period: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            capacity: Maximum number of tokens (requests) available
            refill_rate: Number of tokens to add per refill period
            refill_period: Time period for refilling tokens (seconds)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.refill_period = refill_period
        self.tokens = capacity
        self.last_refill = datetime.now()
        self._lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """
        Acquire tokens from the bucket.
        
        Args:
            tokens: Number of tokens to acquire
            
        Returns:
            True if tokens acquired, False if rate limit exceeded
        """
        async with self._lock:
            # Refill tokens based on elapsed time
            now = datetime.now()
            elapsed = (now - self.last_refill).total_seconds()
            
            if elapsed >= self.refill_period:
                periods = elapsed / self.refill_period
                tokens_to_add = int(periods * self.refill_rate)
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now
            
            # Check if we have enough tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                logger.warning(f"Rate limit exceeded. Available tokens: {self.tokens}")
                return False
    
    def get_wait_time(self) -> float:
        """
        Get time to wait until next token is available.
        
        Returns:
            Wait time in seconds
        """
        if self.tokens >= 1:
            return 0.0
        
        # Calculate when next token will be available
        tokens_needed = 1 - self.tokens
        periods_needed = tokens_needed / self.refill_rate
        return periods_needed * self.refill_period
    
    def reset(self) -> None:
        """Reset the rate limiter to full capacity."""
        self.tokens = self.capacity
        self.last_refill = datetime.now()


class IPRateLimiter:
    """
    Per-IP rate limiter for web requests.
    
    Tracks request rates for individual IP addresses.
    """
    
    def __init__(self, requests_per_minute: int = 60, 
                 cleanup_interval: int = 300):
        """
        Initialize IP rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per IP per minute
            cleanup_interval: Interval to clean up old entries (seconds)
        """
        self.requests_per_minute = requests_per_minute
        self.cleanup_interval = cleanup_interval
        self.requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
        self._last_cleanup = datetime.now()
    
    async def is_allowed(self, ip_address: str) -> bool:
        """
        Check if request from IP is allowed.
        
        Args:
            ip_address: Client IP address
            
        Returns:
            True if request is allowed
        """
        async with self._lock:
            now = datetime.now()
            cutoff = now - timedelta(minutes=1)
            
            # Clean up old requests
            if (now - self._last_cleanup).total_seconds() > self.cleanup_interval:
                self._cleanup_old_requests(cutoff)
                self._last_cleanup = now
            
            # Get recent requests for this IP
            recent_requests = [
                req_time for req_time in self.requests[ip_address]
                if req_time > cutoff
            ]
            
            # Check rate limit
            if len(recent_requests) >= self.requests_per_minute:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return False
            
            # Record this request
            recent_requests.append(now)
            self.requests[ip_address] = recent_requests
            
            return True
    
    def _cleanup_old_requests(self, cutoff: datetime) -> None:
        """Clean up request records older than cutoff time."""
        ips_to_remove = []
        
        for ip, requests in self.requests.items():
            recent = [req for req in requests if req > cutoff]
            if recent:
                self.requests[ip] = recent
            else:
                ips_to_remove.append(ip)
        
        for ip in ips_to_remove:
            del self.requests[ip]
        
        if ips_to_remove:
            logger.debug(f"Cleaned up {len(ips_to_remove)} IP entries")
    
    def get_remaining_requests(self, ip_address: str) -> int:
        """
        Get remaining requests allowed for IP.
        
        Args:
            ip_address: Client IP address
            
        Returns:
            Number of remaining requests
        """
        cutoff = datetime.now() - timedelta(minutes=1)
        recent_requests = [
            req_time for req_time in self.requests.get(ip_address, [])
            if req_time > cutoff
        ]
        return max(0, self.requests_per_minute - len(recent_requests))


# Global rate limiters
_global_limiters: Dict[str, RateLimiter] = {}
_ip_limiter: Optional[IPRateLimiter] = None


def get_rate_limiter(name: str) -> RateLimiter:
    """
    Get or create a named rate limiter.
    
    Args:
        name: Name of the rate limiter
        
    Returns:
        RateLimiter instance
    """
    if name not in _global_limiters:
        # Default configuration
        _global_limiters[name] = RateLimiter(
            capacity=10,
            refill_rate=1.0,
            refill_period=1.0
        )
    
    return _global_limiters[name]


def get_ip_rate_limiter(requests_per_minute: int = 60) -> IPRateLimiter:
    """
    Get global IP rate limiter.
    
    Args:
        requests_per_minute: Maximum requests per IP per minute
        
    Returns:
        IPRateLimiter instance
    """
    global _ip_limiter
    
    if _ip_limiter is None:
        _ip_limiter = IPRateLimiter(requests_per_minute)
    
    return _ip_limiter


def rate_limit_decorator(limiter: RateLimiter, tokens: int = 1):
    """
    Decorator for rate limiting async functions.
    
    Args:
        limiter: RateLimiter instance to use
        tokens: Number of tokens to consume
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not await limiter.acquire(tokens):
                wait_time = limiter.get_wait_time()
                logger.warning(f"Rate limit hit, waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
                # Try again after waiting
                await limiter.acquire(tokens)
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def check_rate_limit(ip_address: str, requests_per_minute: int = 60) -> bool:
    """
    Synchronous helper to check rate limit for an IP.
    
    Args:
        ip_address: Client IP address
        requests_per_minute: Maximum requests per minute
        
    Returns:
        True if request is allowed
    """
    limiter = get_ip_rate_limiter(requests_per_minute)
    
    # Use asyncio.run for sync context
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(limiter.is_allowed(ip_address))
    finally:
        loop.close()

