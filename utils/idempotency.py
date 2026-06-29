"""Idempotency utilities for agent workflows.
Prevents duplicate execution of the same operation.
"""

import redis.asyncio as redis
import json
from typing import Optional, Any


class IdempotencyStore:
    def __init__(self, redis_url: str, ttl: int = 86400):
        self.client = redis.from_url(redis_url)
        self.ttl = ttl

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(f"idempotency:{key}")
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, result: Any):
        await self.client.setex(
            f"idempotency:{key}",
            self.ttl,
            json.dumps(result),
        )

    async def is_processed(self, key: str) -> bool:
        return await self.client.exists(f"idempotency:{key}") > 0
