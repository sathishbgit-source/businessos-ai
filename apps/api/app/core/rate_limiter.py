from __future__ import annotations

import time
from collections import defaultdict
from threading import Lock


class InMemoryRateLimiter:
    """
    Simple in-memory fixed-window rate limiter.

    This implementation is intentionally storage-agnostic so it can
    be replaced by a Redis-backed implementation in a later PR.
    """

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def check(self, client_key: str) -> tuple[bool, int]:
        """
        Check whether a request is allowed.

        Returns:
            (allowed, retry_after_seconds)
        """
        now = time.monotonic()

        with self._lock:
            timestamps = self._requests[client_key]

            cutoff = now - self.window_seconds
            timestamps[:] = [
                timestamp
                for timestamp in timestamps
                if timestamp > cutoff
            ]

            if len(timestamps) >= self.max_requests:
                retry_after = max(
                    1,
                    int(timestamps[0] + self.window_seconds - now),
                )
                return False, retry_after

            timestamps.append(now)

            return True, 0

    def reset(self) -> None:
        """Clear all tracked requests."""
        with self._lock:
            self._requests.clear()
