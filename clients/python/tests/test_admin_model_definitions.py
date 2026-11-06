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

    api.replace_validation_data("definition-1", [{"input_1": "x", "expected_label": "yes"}])

    call = session.request.call_args.kwargs
    assert call["method"] == "PUT"
    assert call["json"][0]["input_1"] == "x"
    assert call["json"][0]["expected_label"] == "yes"


def test_get_validation_data_gets_rows_separately(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'[{"record_key":"row-1"}]',
        headers={'content-type': 'application/json'},
        json=Mock(return_value=[{"record_key": "row-1"}]),
    )
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    assert api.get_validation_data("definition-1") == [{"record_key": "row-1"}]
    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"].endswith("/api/model-definitions/definition-1/validation-data")


def test_applicable_definitions_are_cached_until_mutation(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'[{"_sys_doc_id":"definition-1"}]',
        headers={'content-type': 'application/json'},
        json=Mock(return_value=[{"_sys_doc_id": "definition-1"}]),
    )
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    assert api.get_applicable(co_id="1") == api.get_applicable(co_id="1")
    assert session.request.call_count == 1

    api.replace_validation_data("definition-1", [{"input_1": "x", "expected_label": "yes"}])
    assert session.request.call_count == 2


def test_replace_validation_data_sends_confirmation_only_when_requested(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(status_code=200, content=b'{"rows_saved":0}', headers={'content-type': 'application/json'}, json=Mock(return_value={"rows_saved": 0}))
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    api.replace_validation_data("definition-1", [{"input_1": "x"}])
    assert not session.request.call_args.kwargs.get("params")

    api.replace_validation_data("definition-1", [], confirmed_replace=True)
    call = session.request.call_args.kwargs
    assert call["method"] == "PUT" and call["json"] == []
    assert call["params"] == {"confirmed_replace": "true"}


RECEIPT = {
    "definition_id": "definition-1", "definition_revision": "2026-11-04T10:00:00.123456+00:00",
    "execution_type": "llm", "service_id": "svc-1", "service_revision": "2026-11-03T09:00:00+00:00",
    "selector": "gemini-flash-lite", "vendor": "google", "model_id": "gemini-3.5-flash-lite", "settings": {"seed": 42},
}


def _json_session(body):
    session = Mock()
    session.request.return_value = Mock(status_code=200, content=b'{}', headers={'content-type': 'application/json'},
                                        json=Mock(return_value=body))
    return session


def test_prepare_execution_resolves_for_the_company_and_is_not_cached(base_url: str) -> None:
    session = _json_session(RECEIPT)
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    receipt = api.prepare_execution("definition-1", co_id="42")
    api.prepare_execution("definition-1", co_id="42")

    call = session.request.call_args.kwargs
    assert call["method"] == "GET"
    assert call["url"].endswith("/api/model-definitions/definition-1/execution")
    assert call["headers"]["x-cien-coid"] == "42"
    assert session.request.call_count == 2
    assert receipt["model_id"] == "gemini-3.5-flash-lite"


def test_predict_posts_the_pinned_receipt_revisions(base_url: str) -> None:
    from cien_agent_sdk.transport import hydrate_json_value

    session = _json_session({"content": {"classifications": []}, "metrics": {"input_tokens": 3}})
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))
    # prepare_execution hands back a hydrated receipt; its revisions must go back unchanged
    receipt = hydrate_json_value(RECEIPT)

    result = api.predict("definition-1", co_id="42", receipt=receipt, message="a\n#\nb",
                         output_schema={"type": "object"}, instructions="Batch rules", pipeline_run_id="run-9")

    call = session.request.call_args.kwargs
    assert call["method"] == "POST"
    assert call["url"].endswith("/api/model-definitions/definition-1/predict")
    assert call["headers"]["x-cien-coid"] == "42"
    body = call["json"]
    assert body["service_id"] == "svc-1"
    assert body["definition_revision"].startswith("2026-11-04T10:00:00.123456")
    assert body["service_revision"].startswith("2026-11-03T09:00:00")
    assert body["message"] == "a\n#\nb" and body["instructions"] == "Batch rules"
    assert body["pipeline_run_id"] == "run-9" and body["output_schema"] == {"type": "object"}
    assert set(body) == {"definition_revision", "service_id", "service_revision", "message", "output_schema",
                         "instructions", "pipeline_run_id"}
    assert result["metrics"]["input_tokens"] == 3


def test_selector_errors_surface_the_api_code(base_url: str) -> None:
    import pytest
    from cien_agent_sdk.errors import APIError

    session = Mock()
    detail = {"detail": {"code": "platform_selector_required", "message": "Choose and save a Platform selector"}}
    session.request.return_value = Mock(status_code=409, content=b'{}', headers={'content-type': 'application/json'},
                                        json=Mock(return_value=detail))
    api = AdminModelDefinitionsAPI(HTTPTransport(base_url=base_url, session=session))

    with pytest.raises(APIError) as exc:
        api.prepare_execution("definition-1", co_id="42")
    assert exc.value.status_code == 409
    assert exc.value.response_body["detail"]["code"] == "platform_selector_required"
