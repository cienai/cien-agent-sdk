from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.job_engine_logs import AdminJobEngineLogsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_save_patches_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"task_logs_upserted":1}',
        headers={'content-type': 'application/json'},
        json=Mock(return_value={'task_logs_upserted': 1}),
    )
    api = AdminJobEngineLogsAPI(HTTPTransport(base_url=base_url, session=session))

    api.save(
        'co-1',
        dag_log={'run_id': 'run-1', 'dag_id': 'dag-1'},
        task_logs=[{'task_id': 'task-1', 'dag_id': 'dag-1', 'run_id': 'run-1'}],
    )

    assert session.request.call_args.kwargs['url'].endswith('/api/admin/job-engine-logs/co-1')
    assert session.request.call_args.kwargs['json'] == {
        'dag_log': {'run_id': 'run-1', 'dag_id': 'dag-1'},
        'task_logs': [{'task_id': 'task-1', 'dag_id': 'dag-1', 'run_id': 'run-1'}],
    }
