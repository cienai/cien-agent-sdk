from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests

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
        headers={"X-Default": "1", "Authorization": f"Bearer {clerk_api_token}", "X-Req": "2"},
        timeout=12.5,
    )


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
