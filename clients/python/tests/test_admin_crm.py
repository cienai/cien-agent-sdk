from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.crm import AdminCrmAPI
from cien_agent_sdk.transport import HTTPTransport


def test_describe_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"{}",
        headers={"content-type": "application/json"},
        json=Mock(return_value={}),
    )
    api = AdminCrmAPI(HTTPTransport(base_url=base_url, session=session))

    api.describe(coid="co-1", table="Account", column_names_only=True)

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/crm/describe")
    assert session.request.call_args.kwargs["json"] == {
        "coid": "co-1",
        "table": "Account",
        "column_names_only": True,
    }
