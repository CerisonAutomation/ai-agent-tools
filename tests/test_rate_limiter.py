"""Tests for token-bucket rate limiter."""
import pytest
import asyncio
from utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_acquire_does_not_block_within_burst():
    limiter = RateLimiter(rate=10, burst=5)
    for _ in range(5):
        await limiter.acquire()  # Should complete without sleeping


@pytest.mark.asyncio
async def test_tokens_decrease_after_acquire():
    limiter = RateLimiter(rate=10, burst=5)
    initial = limiter._tokens
    await limiter.acquire()
    assert limiter._tokens < initial
