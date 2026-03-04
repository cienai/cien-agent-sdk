from __future__ import annotations

from unittest.mock import Mock

import pytest

from cien_agent_sdk.admin.sync import AdminSyncAPI
from cien_agent_sdk.transport import HTTPTransport


def test_list_supports_sync_token_filter(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    transport = HTTPTransport(base_url=base_url, session=session)
    api = AdminSyncAPI(transport)

    api.list(sync_token="token-123")

    params = session.request.call_args.kwargs["params"]
    assert params["sync_token"] == "token-123"
    assert "coid" not in params or params["coid"] is None


def test_list_requires_coid_or_sync_token(base_url: str) -> None:
    api = AdminSyncAPI(HTTPTransport(base_url=base_url, session=Mock()))
    with pytest.raises(ValueError, match="Either coid or sync_token is required"):
        api.list()


def test_get_by_sync_token_returns_first_record(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"id":1}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"id": 1}),
    )
    api = AdminSyncAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.get_by_sync_token("token-abc")

    assert result == {"id": 1}
    called_url = session.request.call_args.kwargs["url"]
    assert called_url.endswith("/api/admin/sync/by-token/token-abc")


def test_get_by_sync_token_returns_none_when_not_found(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=404,
        content=b'{"detail":"Sync record not found"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"detail": "Sync record not found"}),
    )
    api = AdminSyncAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.get_by_sync_token("missing-token")

    assert result is None
