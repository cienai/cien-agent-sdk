from __future__ import annotations

import threading
import time

from cien_agent_sdk.metadata_cache import MetadataCache, Stats


def test_get_or_load_caches_value_across_calls() -> None:
    cache = MetadataCache()
    calls = []

    def loader():
        calls.append(1)
        return "value"

    assert cache.get_or_load(("k",), None, loader) == "value"
    assert cache.get_or_load(("k",), None, loader) == "value"

    assert calls == [1]
    assert cache.stats.cache_hits == 1
    assert cache.stats.cache_misses == 1


def test_get_or_load_expires_after_ttl(monkeypatch) -> None:
    cache = MetadataCache()
    calls = []
    fake_now = [1000.0]
    monkeypatch.setattr(time, "monotonic", lambda: fake_now[0])

    def loader():
        calls.append(1)
        return "value"

    assert cache.get_or_load(("k",), 10.0, loader) == "value"
    fake_now[0] += 11.0
    assert cache.get_or_load(("k",), 10.0, loader) == "value"

    assert calls == [1, 1]


def test_get_or_load_never_expires_when_ttl_is_none(monkeypatch) -> None:
    cache = MetadataCache()
    calls = []
    fake_now = [1000.0]
    monkeypatch.setattr(time, "monotonic", lambda: fake_now[0])

    def loader():
        calls.append(1)
        return "value"

    cache.get_or_load(("k",), None, loader)
    fake_now[0] += 10_000_000.0
    cache.get_or_load(("k",), None, loader)

    assert calls == [1]


def test_concurrent_callers_for_same_key_coalesce_into_one_load() -> None:
    cache = MetadataCache(max_concurrency=4)
    call_count = 0
    call_count_lock = threading.Lock()
    ready_to_start = threading.Event()

    def loader():
        nonlocal call_count
        with call_count_lock:
            call_count += 1
        ready_to_start.wait(timeout=5)
        return "value"

    def worker(results, index):
        results[index] = cache.get_or_load(("shared",), None, loader)

    results: dict[int, str] = {}
    threads = [threading.Thread(target=worker, args=(results, i)) for i in range(7)]
    for t in threads:
        t.start()
    time.sleep(0.2)  # give every thread a chance to join the in-flight request
    ready_to_start.set()
    for t in threads:
        t.join(timeout=5)

    assert call_count == 1
    assert all(v == "value" for v in results.values())
    assert cache.stats.coalesced == 6
    assert cache.stats.cache_misses == 1


def test_loader_exception_propagates_to_all_waiters_and_is_not_cached() -> None:
    cache = MetadataCache()
    attempts = []

    def failing_loader():
        attempts.append(1)
        raise ValueError("boom")

    try:
        cache.get_or_load(("k",), None, failing_loader)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # Not cached: a subsequent call retries the loader.
    try:
        cache.get_or_load(("k",), None, failing_loader)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    assert attempts == [1, 1]


def test_invalidate_prefix_drops_only_matching_keys() -> None:
    cache = MetadataCache()
    cache.get_or_load(("mappings", "co-1", "crm_entities"), None, lambda: "a")
    cache.get_or_load(("mappings", "co-1", "crm_mappings", "Account"), None, lambda: "b")
    cache.get_or_load(("mappings", "co-2", "crm_entities"), None, lambda: "c")

    cache.invalidate_prefix(("mappings", "co-1"))

    calls = []
    cache.get_or_load(("mappings", "co-1", "crm_entities"), None, lambda: calls.append(1) or "a2")
    cache.get_or_load(("mappings", "co-2", "crm_entities"), None, lambda: calls.append(1) or "c2")

    # co-1 entry was evicted (reloaded); co-2 entry survived (not reloaded).
    assert calls == [1]


def test_clear_drops_everything() -> None:
    cache = MetadataCache()
    cache.get_or_load(("k1",), None, lambda: "a")
    cache.get_or_load(("k2",), None, lambda: "b")

    cache.clear()

    calls = []
    cache.get_or_load(("k1",), None, lambda: calls.append(1) or "a2")
    cache.get_or_load(("k2",), None, lambda: calls.append(1) or "b2")

    assert calls == [1, 1]


def test_semaphore_bounds_peak_concurrency() -> None:
    cache = MetadataCache(max_concurrency=2)
    active = 0
    active_lock = threading.Lock()
    peak = 0
    peak_lock = threading.Lock()

    def loader_for(key):
        def _loader():
            nonlocal active, peak
            with active_lock:
                active += 1
                with peak_lock:
                    peak = max(peak, active)
            time.sleep(0.1)
            with active_lock:
                active -= 1
            return key
        return _loader

    def worker(key):
        cache.get_or_load((key,), None, loader_for(key))

    threads = [threading.Thread(target=worker, args=(f"key-{i}",)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert peak <= 2
    assert cache.stats.peak_concurrency <= 2
    assert cache.stats.peak_concurrency >= 1


def test_stats_snapshot_reports_all_fields() -> None:
    stats = Stats()
    stats.record_hit()
    stats.record_miss()
    stats.record_coalesced()
    stats.record_concurrency(3)
    stats.record_retry(429)
    stats.record_retry(429)
    stats.record_retry(503)

    snapshot = stats.snapshot()

    assert snapshot == {
        "cache_hits": 1,
        "cache_misses": 1,
        "coalesced": 1,
        "metadata_requests_total": 1,
        "peak_concurrency": 3,
        "retries_by_status": {429: 2, 503: 1},
        "count_429": 2,
    }
    assert stats.count_429 == 2
