from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.mappings import AdminMappingsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_get_crm_mappings_calls_entity_url(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_crm_mappings("co-1", crm_entity="Account")

    called_url = session.request.call_args.kwargs["url"]
    assert called_url.endswith("/api/admin/mappings/co-1/Account")


def test_save_crm_mappings_uses_put(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.save_crm_mappings("co-1", crm_entity="Account", mappings=[{"key": "Id"}])

    assert session.request.call_args.kwargs["method"] == "PUT"


def test_get_crm_mappings_is_cached_for_the_run(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_crm_mappings("co-1", crm_entity="Account")
    api.get_crm_mappings("co-1", crm_entity="Account")

    assert session.request.call_count == 1


def test_list_crm_entities_is_cached_for_the_run(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"crm_entities":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"crm_entities": []}),
    )
    api = AdminMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.list_crm_entities("co-1")
    api.list_crm_entities("co-1")

    assert session.request.call_count == 1


def test_save_crm_mappings_invalidates_cached_mappings_for_coid(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b"[]",
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    transport = HTTPTransport(base_url=base_url, session=session)
    api = AdminMappingsAPI(transport)

    api.get_crm_mappings("co-1", crm_entity="Account")
    api.save_crm_mappings("co-1", crm_entity="Account", mappings=[{"key": "Id"}])
    api.get_crm_mappings("co-1", crm_entity="Account")

    assert session.request.call_count == 3
