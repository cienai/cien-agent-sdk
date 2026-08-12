from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import Mock

import pytest
import requests

import cien_agent_sdk.transport as transport_module
from cien_agent_sdk.errors import APIError, RequestError
from cien_agent_sdk.transport import HTTPTransport


def _response(
    *,
    status_code: int = 200,
    content: bytes = b"",
    headers: dict[str, str] | None = None,
    json_value=None,
    text: str = "",
):
    res = Mock()
    res.status_code = status_code
    res.content = content
    res.headers = headers or {}
    res.text = text
    if isinstance(json_value, Exception):
        res.json.side_effect = json_value
    else:
        res.json.return_value = json_value
    return res


def test_request_builds_url_and_headers_with_token(base_url: str, clerk_api_token: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b'{"ok": true}',
        headers={"content-type": "application/json"},
        json_value={"ok": True},
    )

    transport = HTTPTransport(
        base_url=f"{base_url}/",
        token=clerk_api_token,
        timeout=12.5,
        default_headers={"X-Default": "1"},
        session=session,
    )
    result = transport.request("GET", "/v1/health", headers={"X-Req": "2"})

    assert result == {"ok": True}
    session.request.assert_called_once_with(
        method="GET",
        url=f"{base_url.rstrip('/')}/v1/health",
        params=None,
        json=None,
        data=None,
        files=None,
        headers={
            "X-Default": "1",
            "X-Cien-Client-Id": transport.client_id,
            "Authorization": f"Bearer {clerk_api_token}",
            "X-Req": "2",
        },
        timeout=12.5,
    )


def test_transport_uses_longer_default_timeout(base_url: str) -> None:
    transport = HTTPTransport(base_url=base_url, session=Mock())

    assert transport.timeout == 60.0


def test_request_raises_request_error_on_requests_exception(base_url: str) -> None:
    session = Mock()
    session.request.side_effect = requests.Timeout("timed out")
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(RequestError, match="timed out"):
        transport.request("GET", "/v1/slow")


def test_request_raises_api_error_from_json_detail(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=403,
        content=b'{"detail":"forbidden"}',
        headers={"content-type": "application/json"},
        json_value={"detail": "forbidden"},
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(APIError) as err:
        transport.request("GET", "/v1/protected")

    assert err.value.status_code == 403
    assert err.value.message == "forbidden"
    assert err.value.response_body == {"detail": "forbidden"}


def test_request_retries_transient_401_token_verification_server_error(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=401,
            content=b'{"detail":"Authentication failed: TokenVerificationErrorReason.SERVER_ERROR"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "Authentication failed: TokenVerificationErrorReason.SERVER_ERROR"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert sleep_calls == [5.0]
    assert session.request.call_count == 2


def test_request_does_not_retry_other_401s(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=401,
        content=b'{"detail":"Authentication failed: bad token"}',
        headers={"content-type": "application/json"},
        json_value={"detail": "Authentication failed: bad token"},
    )
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(APIError, match="bad token"):
        transport.request("GET", "/v1/retry")

    assert sleep_calls == []
    assert session.request.call_count == 1


def test_request_raises_api_error_with_text_payload_when_json_parse_fails(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=500,
        content=b"server exploded",
        headers={"content-type": "text/plain"},
        json_value=ValueError("no json"),
        text="server exploded",
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(APIError) as err:
        transport.request("POST", "/v1/work")

    assert err.value.status_code == 500
    assert err.value.message == "server exploded"
    assert err.value.response_body == "server exploded"


def test_request_returns_none_for_no_content(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(status_code=204, content=b"")
    transport = HTTPTransport(base_url=base_url, session=session)

    assert transport.request("DELETE", "/v1/items/1") is None


def test_request_returns_text_for_non_json_content(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b"ok",
        headers={"content-type": "text/plain"},
        text="ok",
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    assert transport.request("GET", "/v1/text") == "ok"


def test_set_token_updates_auth_header_for_next_request(base_url: str, clerk_api_token: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b'{"ok": true}',
        headers={"content-type": "application/json"},
        json_value={"ok": True},
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    transport.set_token(clerk_api_token)
    transport.request("GET", "/v1/health")

    headers = session.request.call_args.kwargs["headers"]
    assert headers["Authorization"] == f"Bearer {clerk_api_token}"


def test_request_hydrates_iso_datetime_and_date_values(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b'{"created_at":"2026-03-12T10:11:12Z","effective_date":"2026-03-01","nested":{"items":["2026-03-12T10:11:12+00:00","plain"]}}',
        headers={"content-type": "application/json"},
        json_value={
            "created_at": "2026-03-12T10:11:12Z",
            "effective_date": "2026-03-01",
            "nested": {"items": ["2026-03-12T10:11:12+00:00", "plain"]},
        },
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/types")

    assert result["created_at"] == datetime(2026, 3, 12, 10, 11, 12, tzinfo=timezone.utc)
    assert result["effective_date"] == date(2026, 3, 1)
    assert result["nested"]["items"][0] == datetime(2026, 3, 12, 10, 11, 12, tzinfo=timezone.utc)
    assert result["nested"]["items"][1] == "plain"


def test_get_retries_on_retryable_statuses_with_default_backoff(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=502,
            content=b'{"detail":"bad gateway"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "bad gateway"},
        ),
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert sleep_calls == [5.0, 10.0]
    assert session.request.call_count == 3


def test_get_retries_on_connection_errors_with_default_backoff(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        requests.Timeout("timed out"),
        requests.ConnectionError("connection dropped"),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert sleep_calls == [5.0, 10.0]
    assert session.request.call_count == 3


def test_get_uses_third_default_backoff_slot_of_thirty_seconds(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=502,
            content=b'{"detail":"bad gateway"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "bad gateway"},
        ),
        _response(
            status_code=502,
            content=b'{"detail":"bad gateway"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "bad gateway"},
        ),
        _response(
            status_code=504,
            content=b'{"detail":"gateway timeout"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "gateway timeout"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert sleep_calls == [5.0, 10.0, 30.0]
    assert session.request.call_count == 4


def test_get_raises_after_exhausting_retry_budget(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(APIError, match="unavailable"):
        transport.request("GET", "/v1/retry")

    assert sleep_calls == [5.0, 10.0, 30.0]
    assert session.request.call_count == 4


def test_non_get_requests_do_not_retry(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=502,
        content=b'{"detail":"bad gateway"}',
        headers={"content-type": "application/json"},
        json_value={"detail": "bad gateway"},
    )
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    transport = HTTPTransport(base_url=base_url, session=session)

    with pytest.raises(APIError, match="bad gateway"):
        transport.request("POST", "/v1/retry")

    assert sleep_calls == []
    assert session.request.call_count == 1


def test_non_get_requests_retry_when_explicitly_marked_retryable(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=502,
            content=b'{"detail":"bad gateway"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "bad gateway"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("POST", "/v1/retry", retryable=True)

    assert result == {"ok": True}
    assert sleep_calls == [5.0]
    assert session.request.call_count == 2


def test_non_get_requests_retry_connection_errors_when_explicitly_marked_retryable(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        requests.Timeout("timed out"),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    monkeypatch.setattr(transport_module.random, "uniform", lambda a, b: 0.0)
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("POST", "/v1/retry", retryable=True)

    assert result == {"ok": True}
    assert sleep_calls == [5.0]
    assert session.request.call_count == 2


def test_retry_backoff_includes_bounded_jitter(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=502,
            content=b'{"detail":"bad gateway"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "bad gateway"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    transport = HTTPTransport(base_url=base_url, session=session)

    transport.request("GET", "/v1/retry")

    assert len(sleep_calls) == 1
    # base delay is 5.0s with up to 20% jitter added, never subtracted.
    assert 5.0 <= sleep_calls[0] <= 6.0


def test_retry_after_seconds_header_overrides_computed_backoff(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=429,
            content=b'{"detail":"rate limited"}',
            headers={"content-type": "application/json", "Retry-After": "2"},
            json_value={"detail": "rate limited"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert sleep_calls == [2.0]


def test_retry_after_http_date_header_overrides_computed_backoff(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    future = datetime.now(timezone.utc).replace(microsecond=0)
    from datetime import timedelta

    future = future + timedelta(seconds=3)
    retry_after_value = future.strftime("%a, %d %b %Y %H:%M:%S GMT")
    session.request.side_effect = [
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json", "Retry-After": retry_after_value},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    sleep_calls: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))
    transport = HTTPTransport(base_url=base_url, session=session)

    result = transport.request("GET", "/v1/retry")

    assert result == {"ok": True}
    assert len(sleep_calls) == 1
    assert 0.0 <= sleep_calls[0] <= 4.0


def test_retries_are_recorded_by_status_in_stats(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    session = Mock()
    session.request.side_effect = [
        _response(
            status_code=429,
            content=b'{"detail":"rate limited"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "rate limited"},
        ),
        _response(
            status_code=429,
            content=b'{"detail":"rate limited"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "rate limited"},
        ),
        _response(
            status_code=503,
            content=b'{"detail":"unavailable"}',
            headers={"content-type": "application/json"},
            json_value={"detail": "unavailable"},
        ),
        _response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            json_value={"ok": True},
        ),
    ]
    monkeypatch.setattr(transport_module.time, "sleep", lambda seconds: None)
    transport = HTTPTransport(base_url=base_url, session=session)

    transport.request("GET", "/v1/retry")

    assert transport.stats.retries_by_status == {429: 2, 503: 1}
    assert transport.stats.count_429 == 2


def test_does_not_retry_400_401_or_404(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail_on_sleep(_seconds):
        raise AssertionError("should not sleep")

    monkeypatch.setattr(transport_module.time, "sleep", _fail_on_sleep)
    for status_code, detail in [(400, "bad request"), (401, "missing credentials"), (404, "not found")]:
        session = Mock()
        session.request.return_value = _response(
            status_code=status_code,
            content=b'{"detail":"%s"}' % detail.encode(),
            headers={"content-type": "application/json"},
            json_value={"detail": detail},
        )
        transport = HTTPTransport(base_url=base_url, session=session)

        with pytest.raises(APIError) as err:
            transport.request("GET", "/v1/retry")

        assert err.value.status_code == status_code
        assert session.request.call_count == 1


def test_transport_emits_stable_client_id_header_by_default(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b'{"ok": true}',
        headers={"content-type": "application/json"},
        json_value={"ok": True},
    )
    transport = HTTPTransport(base_url=base_url, session=session)

    transport.request("GET", "/v1/health")
    first_headers = session.request.call_args.kwargs["headers"]
    transport.request("GET", "/v1/health")
    second_headers = session.request.call_args.kwargs["headers"]

    assert first_headers["X-Cien-Client-Id"]
    assert first_headers["X-Cien-Client-Id"] == second_headers["X-Cien-Client-Id"]
    assert "X-Cien-Run-Id" not in first_headers


def test_transport_includes_run_id_header_when_set(base_url: str) -> None:
    session = Mock()
    session.request.return_value = _response(
        status_code=200,
        content=b'{"ok": true}',
        headers={"content-type": "application/json"},
        json_value={"ok": True},
    )
    transport = HTTPTransport(base_url=base_url, session=session, client_id="fixed-client", run_id="run-42")

    transport.request("GET", "/v1/health")

    headers = session.request.call_args.kwargs["headers"]
    assert headers["X-Cien-Client-Id"] == "fixed-client"
    assert headers["X-Cien-Run-Id"] == "run-42"

    transport.set_run_id(None)
    transport.request("GET", "/v1/health")
    headers = session.request.call_args.kwargs["headers"]
    assert "X-Cien-Run-Id" not in headers


def test_transport_exposes_metadata_cache_and_enable_flag(base_url: str) -> None:
    transport = HTTPTransport(base_url=base_url, session=Mock(), enable_metadata_cache=False, metadata_max_concurrency=2)

    assert transport.enable_metadata_cache is False
    assert transport.metadata_cache is not None
