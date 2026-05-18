from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.public.schemas import PublicSchemasAPI
from cien_agent_sdk.transport import HTTPTransport


def test_get_base_schema_uses_expected_path(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"type":"struct","fields":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"type": "struct", "fields": []}),
    )
    api = PublicSchemasAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.get_base_schema("companies")

    assert result == {"type": "struct", "fields": []}
    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"] == f"{base_url.rstrip('/')}/api/schemas/base/companies"


def test_load_schema_uses_expected_path(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"type":"struct","fields":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"type": "struct", "fields": []}),
    )
    api = PublicSchemasAPI(HTTPTransport(base_url=base_url, session=session))

    api.load_schema(coid="co-1", cien_entity="companies")

    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"] == f"{base_url.rstrip('/')}/api/schemas/co-1/companies"


def test_get_schema_uses_expected_path(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"type":"struct","fields":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"type": "struct", "fields": []}),
    )
    api = PublicSchemasAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_schema(coid="co-1", cien_entity="companies", crm_type="salesforce")

    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"] == f"{base_url.rstrip('/')}/api/schemas/co-1/companies/generated"
    assert call["params"] == {"crm_type": "salesforce"}


def test_initialize_schemas_sends_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"message":"ok"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"message": "ok"}),
    )
    api = PublicSchemasAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.initialize_schemas(coid="co-1", crm_type="salesforce")

    assert result == {"message": "ok"}
    call = session.request.call_args.kwargs
    assert call["method"] == "POST"
    assert call["url"] == f"{base_url.rstrip('/')}/api/schemas/co-1/initialize"
    assert call["params"] == {"crm_type": "salesforce"}


def test_initialize_schemas_marks_request_retryable(base_url: str) -> None:
    transport = Mock(spec=HTTPTransport)
    transport.request.return_value = {"message": "ok"}
    api = PublicSchemasAPI(transport)

    result = api.initialize_schemas(coid="co-1", crm_type="salesforce")

    assert result == {"message": "ok"}
    transport.request.assert_called_once_with(
        "POST",
        "/api/schemas/co-1/initialize",
        json=None,
        params={"crm_type": "salesforce"},
        data=None,
        files=None,
        retryable=True,
    )
