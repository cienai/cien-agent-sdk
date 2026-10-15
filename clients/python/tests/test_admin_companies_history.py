from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.companies_history import AdminCompaniesHistoryAPI
from cien_agent_sdk.transport import HTTPTransport


def _api(base_url: str) -> tuple[AdminCompaniesHistoryAPI, Mock]:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"job_status":"failed"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"job_status": "failed"}),
    )
    return AdminCompaniesHistoryAPI(HTTPTransport(base_url=base_url, session=session)), session


def test_get_for_export_uses_export_path(base_url: str) -> None:
    api, session = _api(base_url)

    result = api.get_for_export("co-1", selected_columns=["job_status"])

    assert result == {"job_status": "failed"}
    kwargs = session.request.call_args.kwargs
    assert kwargs["url"].endswith("/api/admin/companies-history/co-1/export")
    assert kwargs["params"]["selected_columns"] == ["job_status"]


def test_get_still_uses_the_general_path(base_url: str) -> None:
    api, session = _api(base_url)

    api.get("co-1")

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/companies-history/co-1")
