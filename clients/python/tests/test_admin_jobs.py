from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.jobs import AdminJobsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_run_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"message":"ok"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"message": "ok"}),
    )
    api = AdminJobsAPI(HTTPTransport(base_url=base_url, session=session))

    api.run(coid="co-1", job_type="export", priority=True)

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/jobs/run")
    assert session.request.call_args.kwargs["json"] == {
        "coid": "co-1",
        "jobType": "export",
        "priority": True,
    }


def test_list_sends_limit_param_when_provided(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminJobsAPI(HTTPTransport(base_url=base_url, session=session))

    api.list("co-1", limit=25)

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/jobs/co-1")
    assert session.request.call_args.kwargs["params"] == {"limit": 25}


def test_cancel_posts_expected_path(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"message":"ok"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"message": "ok"}),
    )
    api = AdminJobsAPI(HTTPTransport(base_url=base_url, session=session))

    api.cancel(coid="co-1", dag_run_id="run-1")

    assert session.request.call_args.kwargs["url"].endswith("/api/admin/jobs/co-1/run-1/cancel")
    assert session.request.call_args.kwargs["json"] is None
