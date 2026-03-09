from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.public.config import PublicConfigAPI
from cien_agent_sdk.transport import HTTPTransport


def test_list_passes_expected_query_params(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = PublicConfigAPI(HTTPTransport(base_url=base_url, session=session))

    api.list(coid="co-1", key="currency", level="company", convert_dtypes=True)

    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"] == f"{base_url.rstrip('/')}/api/config"
    assert call["params"] == {
        "coid": "co-1",
        "key": "currency",
        "level": "company",
        "convert_dtypes": True,
    }


def test_update_sends_bulk_config_payload_with_put(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'[{"key":"currency","value":"USD"}]',
        headers={"content-type": "application/json"},
        json=Mock(return_value=[{"key": "currency", "value": "USD"}]),
    )
    api = PublicConfigAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.update(
        coid="co-1",
        config=[
            {"key": "currency", "type": "string", "value": "USD"},
            {"key": "timezone", "type": "string", "value": "UTC"},
        ],
    )

    assert result == [{"key": "currency", "value": "USD"}]
    call = session.request.call_args.kwargs
    assert call["method"] == "PUT"
    assert call["url"] == f"{base_url.rstrip('/')}/api/config/co-1"
    assert call["json"] == {
        "config": [
            {"key": "currency", "type": "string", "value": "USD"},
            {"key": "timezone", "type": "string", "value": "UTC"},
        ]
    }
