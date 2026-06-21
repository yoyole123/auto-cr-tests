"""Naive in-memory, per-client rate limiter."""
import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

WINDOW_SECONDS = 60
MAX_REQUESTS = 100

_hits: dict[str, list[float]] = defaultdict(list)


async def rate_limit(request: Request) -> None:
    """Reject the request if the client exceeded its per-window quota."""
    client = request.client.host if request.client else "unknown"
    now = time.time()
    recent = [t for t in _hits[client] if now - t < WINDOW_SECONDS]
    if len(recent) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
    recent.append(now)
    _hits[client] = recent
