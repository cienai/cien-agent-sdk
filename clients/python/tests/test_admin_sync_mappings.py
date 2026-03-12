from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.sync_mappings import AdminSyncMappingsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_get_mapping_type_calls_sync_scoped_url(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"mapping_type":"salesforce"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"mapping_type": "salesforce"}),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_mapping_type(7)

    called_url = session.request.call_args.kwargs["url"]
    assert called_url.endswith("/api/admin/sync-mappings/7/mapping-type")


def test_set_mapping_type_uses_put_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"mapping_type":"hubspot"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"mapping_type": "hubspot"}),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.set_mapping_type(9, mapping_type="hubspot")

    assert session.request.call_args.kwargs["method"] == "PUT"
    assert session.request.call_args.kwargs["json"] == {"mapping_type": "hubspot"}


def test_get_cien_entity_sends_query_param(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"cien_entity":"accounts"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"cien_entity": "accounts"}),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_cien_entity(10, crm_entity="Account")

    assert session.request.call_args.kwargs["params"] == {"crm_entity": "Account"}


def test_set_entity_overrides_uses_put_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"entity_overrides":{"Lead":"people"}}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"entity_overrides": {"Lead": "people"}}),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.set_entity_overrides(11, entity_overrides={"Lead": "people"})

    assert session.request.call_args.kwargs["method"] == "PUT"
    assert session.request.call_args.kwargs["json"] == {"entity_overrides": {"Lead": "people"}}


def test_get_default_mapping_sends_query_param(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"default_mapping":[]}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"default_mapping": []}),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.get_default_mapping(12, crm_entity="Contact")

    called_url = session.request.call_args.kwargs["url"]
    assert called_url.endswith("/api/admin/sync-mappings/12/default-mapping")
    assert session.request.call_args.kwargs["params"] == {"crm_entity": "Contact"}


def test_set_mapping_targets_entity_url(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'[]',
        headers={"content-type": "application/json"},
        json=Mock(return_value=[]),
    )
    api = AdminSyncMappingsAPI(HTTPTransport(base_url=base_url, session=session))

    api.set_mapping(13, crm_entity="Account", mappings=[{"key": "Id"}])

    called_url = session.request.call_args.kwargs["url"]
    assert session.request.call_args.kwargs["method"] == "PUT"
    assert called_url.endswith("/api/admin/sync-mappings/13/mappings/Account")
    assert session.request.call_args.kwargs["json"] == {"mappings": [{"key": "Id"}]}
