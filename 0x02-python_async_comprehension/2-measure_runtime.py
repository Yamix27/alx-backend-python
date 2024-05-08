#!/usr/bin/env python3
"""
measure the runtime of executing multiple
async modules concurrently.
"""
import asyncio
import time

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    measure the runtime of executing multiple
    async comprehensions concurrently.
    Returns:
        float: The total runtime in seconds.
    """
    go = time.perf_counter()
    await asyncio.gather(async_comprehension(), async_comprehension(),
                         async_comprehension(), async_comprehension()
                         )
    stop = time.perf_counter()
    return stop - go
