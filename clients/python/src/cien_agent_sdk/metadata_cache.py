"""Job-scoped metadata caching, single-flight coalescing, and transport stats.

`MetadataCache` is owned by one `HTTPTransport` instance, which in normal SDK
usage means one cache per pipeline run (one `CienClient` per job). Endpoint
groups opt into caching per-method via `EndpointGroup._get_cached`; nothing is
cached unless explicitly wired up, and mutations must explicitly invalidate
the keys they affect via `EndpointGroup._invalidate_cache`.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Callable


class Stats:
    """Thread-safe counters for cache and retry observability."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.cache_hits = 0
        self.cache_misses = 0
        self.coalesced = 0
        self.peak_concurrency = 0
        self.retries_by_status: dict[int, int] = {}

    def record_hit(self) -> None:
        with self._lock:
            self.cache_hits += 1

    def record_miss(self) -> None:
        with self._lock:
            self.cache_misses += 1

    def record_coalesced(self) -> None:
        with self._lock:
            self.coalesced += 1

    def record_concurrency(self, active: int) -> None:
        with self._lock:
            if active > self.peak_concurrency:
                self.peak_concurrency = active

    def record_retry(self, status_code: int) -> None:
        with self._lock:
            self.retries_by_status[status_code] = self.retries_by_status.get(status_code, 0) + 1

    @property
    def count_429(self) -> int:
        with self._lock:
            return self.retries_by_status.get(429, 0)

    @property
    def metadata_requests_total(self) -> int:
        """Real outbound metadata requests issued (cache misses; coalesced callers don't count)."""
        with self._lock:
            return self.cache_misses

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "coalesced": self.coalesced,
                "metadata_requests_total": self.cache_misses,
                "peak_concurrency": self.peak_concurrency,
                "retries_by_status": dict(self.retries_by_status),
                "count_429": self.retries_by_status.get(429, 0),
            }


class _Waiter:
    __slots__ = ("event", "value", "error")

    def __init__(self) -> None:
        self.event = threading.Event()
        self.value: Any = None
        self.error: BaseException | None = None


class MetadataCache:
    """TTL cache with single-flight coalescing and a bounded concurrency gate."""

    def __init__(self, *, max_concurrency: int = 4, stats: Stats | None = None) -> None:
        self._lock = threading.Lock()
        self._entries: dict[tuple, tuple[Any, float | None]] = {}
        self._inflight: dict[tuple, _Waiter] = {}
        self._semaphore = threading.BoundedSemaphore(max(1, max_concurrency))
        self._active = 0
        self.stats = stats if stats is not None else Stats()

    def get_or_load(self, key: tuple, ttl: float | None, loader: Callable[[], Any]) -> Any:
        """Return the cached value for `key`, loading it at most once concurrently."""
        now = time.monotonic()
        with self._lock:
            cached = self._entries.get(key)
            if cached is not None:
                value, expires_at = cached
                if expires_at is None or expires_at > now:
                    self.stats.record_hit()
                    return value
                del self._entries[key]

            waiter = self._inflight.get(key)
            if waiter is not None:
                is_leader = False
            else:
                waiter = _Waiter()
                self._inflight[key] = waiter
                is_leader = True

        if not is_leader:
            self.stats.record_coalesced()
            waiter.event.wait()
            if waiter.error is not None:
                raise waiter.error
            return waiter.value

        self.stats.record_miss()
        try:
            with self._semaphore:
                with self._lock:
                    self._active += 1
                    active = self._active
                self.stats.record_concurrency(active)
                try:
                    value = loader()
                finally:
                    with self._lock:
                        self._active -= 1
        except BaseException as exc:  # noqa: BLE001 - propagate to all waiters
            waiter.error = exc
            with self._lock:
                del self._inflight[key]
            waiter.event.set()
            raise

        waiter.value = value
        with self._lock:
            expires_at = None if ttl is None else now + ttl
            self._entries[key] = (value, expires_at)
            del self._inflight[key]
        waiter.event.set()
        return value

    def invalidate_prefix(self, prefix: tuple) -> None:
        """Drop every cached key that starts with `prefix`."""
        prefix_len = len(prefix)
        with self._lock:
            stale = [k for k in self._entries if k[:prefix_len] == prefix]
            for k in stale:
                del self._entries[k]

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
