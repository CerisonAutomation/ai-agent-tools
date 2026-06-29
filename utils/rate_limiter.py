"""
Token-bucket rate limiter for outbound API calls.
Prevents 429s from Guesty and other rate-limited APIs.
"""

import asyncio
import time
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter.
    rate: requests per second
    burst: max burst size
    """
    def __init__(self, rate: float, burst: int):
        self.rate  = rate
        self.burst = burst
        self._tokens = burst
        self._last   = time.monotonic()
        self._lock   = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
            self._last = now

            if self._tokens < 1:
                wait = (1 - self._tokens) / self.rate
                logger.debug(f"Rate limit: waiting {wait:.2f}s")
                await asyncio.sleep(wait)
                self._tokens = 0
            else:
                self._tokens -= 1
