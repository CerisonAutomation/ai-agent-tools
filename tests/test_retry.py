"""Tests for async retry decorator."""
import pytest
from utils.retry import async_retry


@pytest.mark.asyncio
async def test_succeeds_on_first_attempt():
    call_count = 0

    @async_retry(max_attempts=3)
    async def fn():
        nonlocal call_count
        call_count += 1
        return "ok"

    result = await fn()
    assert result == "ok"
    assert call_count == 1


@pytest.mark.asyncio
async def test_retries_on_failure_then_succeeds():
    call_count = 0

    @async_retry(max_attempts=3, base_delay=0.01)
    async def fn():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("transient")
        return "ok"

    result = await fn()
    assert result == "ok"
    assert call_count == 3


@pytest.mark.asyncio
async def test_raises_after_max_attempts():
    @async_retry(max_attempts=2, base_delay=0.01)
    async def fn():
        raise RuntimeError("always fails")

    with pytest.raises(RuntimeError):
        await fn()
