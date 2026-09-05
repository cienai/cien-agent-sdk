from unittest.mock import Mock

from cien_agent_sdk.admin.model_definitions import AdminModelDefinitionsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_list_model_definitions_passes_scope_params(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(status_code=200, content=b'[]', headers={'content-type': 'application/json'}, json=Mock(return_value=[]))
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    api.list(scope_type="partner", partner_id=7)

    call = session.request.call_args.kwargs
    assert call["url"].endswith("/api/model-definitions")
    assert call["params"] == {"scope_type": "partner", "partner_id": 7}


def test_replace_validation_data_puts_flexible_rows(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(status_code=200, content=b'{"rows_saved":1}', headers={'content-type': 'application/json'}, json=Mock(return_value={"rows_saved": 1}))
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    api.replace_validation_data("definition-1", [{"input_data_1": {"text": "x"}, "expected_output": "yes"}])

    call = session.request.call_args.kwargs
    assert call["method"] == "PUT"
    assert call["json"][0]["expected_output"] == "yes"
