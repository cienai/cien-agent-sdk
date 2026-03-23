from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.job_data import AdminJobDataAPI
from cien_agent_sdk.transport import HTTPTransport


def test_create_posts_expected_path(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"result":{"key":"job_data_conn"}}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"result": {"key": "job_data_conn"}}),
    )
    api = AdminJobDataAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.create(coid="co-1")

    assert result == {"result": {"key": "job_data_conn"}}
    assert session.request.call_args.kwargs["url"].endswith("/api/admin/job-data/co-1/create")
    assert session.request.call_args.kwargs["json"] is None


def test_refresh_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"result":{"key":"job_data_conn"}}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"result": {"key": "job_data_conn"}}),
    )
    api = AdminJobDataAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.refresh(coid="co-1", region="us")

    assert result == {"result": {"key": "job_data_conn"}}
    assert session.request.call_args.kwargs["url"].endswith("/api/admin/job-data/co-1/refresh")
    assert session.request.call_args.kwargs["json"] == {"region": "us"}


def test_save_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"key":"job_data_conn"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"key": "job_data_conn"}),
    )
    api = AdminJobDataAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.save(coid="co-1", value={"BUCKET_URI": "wasbs://x"}, config_type="string")

    assert result == {"key": "job_data_conn"}
    assert session.request.call_args.kwargs["url"].endswith("/api/admin/job-data/co-1")
    assert session.request.call_args.kwargs["json"] == {
        "value": {"BUCKET_URI": "wasbs://x"},
        "type": "string",
    }


def test_explore_gets_expected_params(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"items":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"items": []}),
    )
    api = AdminJobDataAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.explore(
        coid="co-1",
        prefix="config",
        limit=500,
        recursive=True,
    )

    assert result == {"items": []}
    assert session.request.call_args.kwargs["url"].endswith("/api/admin/job-data/co-1/explore")
    assert session.request.call_args.kwargs["params"] == {
        "prefix": "config",
        "limit": 500,
        "recursive": True,
    }


def test_sizes_gets_expected_params(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"container_total_size_bytes":100}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"container_total_size_bytes": 100}),
    )
    api = AdminJobDataAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.sizes(
        coid="co-1",
        prefix="config",
        include_container_total=True,
    )

    assert result == {"container_total_size_bytes": 100}
    assert session.request.call_args.kwargs["url"].endswith("/api/admin/job-data/co-1/sizes")
    assert session.request.call_args.kwargs["params"] == {
        "prefix": "config",
        "include_container_total": True,
    }
