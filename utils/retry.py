"""
Exponential backoff retry decorator for async functions.
Used across all workflow API calls to handle transient failures.
"""

import asyncio
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)


def async_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """Decorator: retry async function with exponential backoff."""
    def decorator(fn: Callable):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            attempt = 0
            delay = base_delay
            while attempt < max_attempts:
                try:
                    return await fn(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"{fn.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f"{fn.__name__} attempt {attempt} failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                    delay *= backoff
        return wrapper
    return decorator
