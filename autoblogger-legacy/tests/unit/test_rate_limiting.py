"""
Tests for rate limiting functionality.

Validates rate limiter behavior, token bucket algorithm,
and IP-based rate limiting.
"""

import pytest
import asyncio
from datetime import datetime

from src.security.rate_limiting import (
    RateLimiter,
    IPRateLimiter,
    get_rate_limiter,
    rate_limit_decorator
)


class TestRateLimiter:
    """Test rate limiter functionality."""
    
    @pytest.mark.asyncio
    async def test_rate_limiter_basic(self):
        """Test basic rate limiting."""
        limiter = RateLimiter(capacity=5, refill_rate=1.0, refill_period=1.0)
        
        # Should allow first 5 requests
        for i in range(5):
            assert await limiter.acquire(1) == True
        
        # 6th request should be denied
        assert await limiter.acquire(1) == False
    
    @pytest.mark.asyncio
    async def test_rate_limiter_refill(self):
        """Test rate limiter token refill."""
        limiter = RateLimiter(capacity=2, refill_rate=2.0, refill_period=0.1)
        
        # Use all tokens
        assert await limiter.acquire(2) == True
        assert await limiter.acquire(1) == False
        
        # Wait for refill
        await asyncio.sleep(0.15)
        
        # Should have refilled
        assert await limiter.acquire(2) == True
    
    @pytest.mark.asyncio
    async def test_rate_limiter_reset(self):
        """Test rate limiter reset."""
        limiter = RateLimiter(capacity=5, refill_rate=1.0)
        
        # Use all tokens
        for i in range(5):
            await limiter.acquire(1)
        
        # Reset
        limiter.reset()
        
        # Should allow requests again
        assert await limiter.acquire(1) == True
    
    def test_rate_limiter_get_wait_time(self):
        """Test wait time calculation."""
        limiter = RateLimiter(capacity=5, refill_rate=1.0, refill_period=1.0)
        
        # With full capacity, wait time should be 0
        assert limiter.get_wait_time() == 0.0


class TestIPRateLimiter:
    """Test IP-based rate limiting."""
    
    @pytest.mark.asyncio
    async def test_ip_rate_limiter_basic(self):
        """Test basic IP rate limiting."""
        limiter = IPRateLimiter(requests_per_minute=5)
        
        # Should allow first 5 requests from same IP
        for i in range(5):
            assert await limiter.is_allowed("192.168.1.1") == True
        
        # 6th request should be denied
        assert await limiter.is_allowed("192.168.1.1") == False
    
    @pytest.mark.asyncio
    async def test_ip_rate_limiter_different_ips(self):
        """Test rate limiting with different IPs."""
        limiter = IPRateLimiter(requests_per_minute=5)
        
        # Each IP should have its own limit
        for i in range(5):
            assert await limiter.is_allowed("192.168.1.1") == True
        for i in range(5):
            assert await limiter.is_allowed("192.168.1.2") == True
        
        # Both should be limited now
        assert await limiter.is_allowed("192.168.1.1") == False
        assert await limiter.is_allowed("192.168.1.2") == False
    
    def test_ip_rate_limiter_remaining_requests(self):
        """Test remaining requests calculation."""
        limiter = IPRateLimiter(requests_per_minute=10)
        
        # Should have full capacity
        assert limiter.get_remaining_requests("192.168.1.1") == 10


class TestRateLimitDecorator:
    """Test rate limit decorator."""
    
    @pytest.mark.asyncio
    async def test_rate_limit_decorator_allows_requests(self):
        """Test decorator allows requests within limit."""
        limiter = RateLimiter(capacity=5, refill_rate=1.0)
        
        @rate_limit_decorator(limiter, tokens=1)
        async def test_function():
            return "success"
        
        # Should allow requests
        for i in range(5):
            result = await test_function()
            assert result == "success"
    
    @pytest.mark.asyncio
    async def test_rate_limit_decorator_waits(self):
        """Test decorator waits when limit exceeded."""
        limiter = RateLimiter(capacity=1, refill_rate=10.0, refill_period=0.1)
        
        @rate_limit_decorator(limiter, tokens=1)
        async def test_function():
            return "success"
        
        # First call should succeed immediately
        result = await test_function()
        assert result == "success"
        
        # Second call should wait but eventually succeed
        start = datetime.now()
        result = await test_function()
        duration = (datetime.now() - start).total_seconds()
        
        assert result == "success"
        assert duration >= 0.09  # Should have waited ~0.1s

