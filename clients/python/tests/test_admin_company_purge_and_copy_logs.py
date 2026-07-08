from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.admin.company_purge_and_copy_logs import AdminCompanyPurgeAndCopyLogsAPI
from cien_agent_sdk.transport import HTTPTransport


def test_create_posts_expected_payload(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"coid":"co-1"}',
        headers={'content-type': 'application/json'},
        json=Mock(return_value={'coid': 'co-1'}),
    )
    api = AdminCompanyPurgeAndCopyLogsAPI(HTTPTransport(base_url=base_url, session=session))

    api.create('co-1', user='user-1', reason='reason-1', event='purge_staging', status='success')

    assert session.request.call_args.kwargs['url'].endswith('/api/admin/company-purge-and-copy-logs/co-1')
    assert session.request.call_args.kwargs['json'] == {
        'user': 'user-1', 'reason': 'reason-1', 'event': 'purge_staging', 'status': 'success',
    }
