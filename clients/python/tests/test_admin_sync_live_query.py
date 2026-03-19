from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.sync_live_query import AdminSyncLiveQueryAPI
from cien_agent_sdk.transport import HTTPTransport


def test_describe_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"{}",
        headers={"content-type": "application/json"},
        json=Mock(return_value={}),
    )
    api = AdminSyncLiveQueryAPI(HTTPTransport(base_url=base_url, session=session))

    api.describe(coid="co-1", crm_entity="Account", column_names_only=True)

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/sync_live_query/describe")
    assert session.request.call_args.kwargs["json"] == {
        "coid": "co-1",
        "crm_entity": "Account",
        "column_names_only": True,
    }


def test_query_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminSyncLiveQueryAPI(HTTPTransport(base_url=base_url, session=session))

    api.query(coid="co-1", crm_entity="Account", query="SELECT Id FROM Account", limit="LIMIT 10")

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/sync_live_query/query")
    assert session.request.call_args.kwargs["json"] == {
        "coid": "co-1",
        "crm_entity": "Account",
        "query": "SELECT Id FROM Account",
        "limit": "LIMIT 10",
    }
