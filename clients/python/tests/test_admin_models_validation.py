from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.models_validation import AdminModelsValidationAPI
from cien_agent_sdk.transport import HTTPTransport


def test_save_many_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"rows_inserted":1}',
        headers={'content-type': 'application/json'},
        json=Mock(return_value={'rows_inserted': 1}),
    )
    api = AdminModelsValidationAPI(HTTPTransport(base_url=base_url, session=session))

    api.save_many([{'model_name': 'account_type', 'metric_name': 'accuracy'}])

    assert session.request.call_args.kwargs['url'].endswith('/api/admin/models-validation')
    assert session.request.call_args.kwargs['json'] == {
        'rows': [{'model_name': 'account_type', 'metric_name': 'accuracy'}],
    }
