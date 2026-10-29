from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.model_validation_runs import AdminModelValidationRunsAPI
from cien_agent_sdk.transport import HTTPTransport


def _api(base_url: str, body: dict) -> tuple[AdminModelValidationRunsAPI, Mock]:
    session = Mock()
    session.request.return_value = Mock(status_code=200, content=b'{}', headers={'content-type': 'application/json'},
                                        json=Mock(return_value=body))
    return AdminModelValidationRunsAPI(HTTPTransport(base_url=base_url, session=session)), session


def test_start_pins_the_definition_for_a_dag_run(base_url: str) -> None:
    api, session = _api(base_url, {'run': {'_sys_doc_id': 'run-1'}, 'definition': {}, 'completed': False})

    result = api.start(model_definition_id='def-1', dag_run_id='manual__1', dag_id='models_validation',
                       llm_model_name='gemini-3.5-flash-lite', provider='google')

    assert result['run']['_sys_doc_id'] == 'run-1'
    assert session.request.call_args.kwargs['method'] == 'POST'
    assert session.request.call_args.kwargs['url'].endswith('/api/admin/model-validation-runs')
    assert session.request.call_args.kwargs['json'] == {
        'model_definition_id': 'def-1', 'dag_run_id': 'manual__1', 'dag_id': 'models_validation',
        'llm_model_name': 'gemini-3.5-flash-lite', 'provider': 'google',
    }


def test_finish_posts_status_and_outcomes(base_url: str) -> None:
    api, session = _api(base_url, {'status': 'success'})

    api.finish('run-1', status='success', outcomes=[{'validation_row_id': 'r1', 'is_correct': True}])

    assert session.request.call_args.kwargs['url'].endswith('/api/admin/model-validation-runs/run-1/finish')
    assert session.request.call_args.kwargs['json'] == {
        'status': 'success', 'error_message': None, 'outcomes': [{'validation_row_id': 'r1', 'is_correct': True}],
        'llm_model_name': None, 'provider': None,
    }


def test_reads_use_the_scoped_model_definition_routes(base_url: str) -> None:
    api, session = _api(base_url, {})

    api.compare(baseline_run_id='a', candidate_run_id='b')
    assert session.request.call_args.kwargs['url'].endswith('/api/model-definitions/validation-runs/compare')
    assert session.request.call_args.kwargs['params'] == {'baseline_run_id': 'a', 'candidate_run_id': 'b'}
    api.failed_examples('run-1', page=2)
    assert session.request.call_args.kwargs['url'].endswith('/api/model-definitions/validation-runs/run-1/failed-examples')
    api.list('def-1')
    assert session.request.call_args.kwargs['url'].endswith('/api/model-definitions/def-1/validation-runs')
