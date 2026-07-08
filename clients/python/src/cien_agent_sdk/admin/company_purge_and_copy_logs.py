from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminCompanyPurgeAndCopyLogsAPI(EndpointGroup):
    """/api/admin/company-purge-and-copy-logs endpoints."""

    def create(self, coid: str, *, user: str, reason: str = '', event: str, status: str) -> dict[str, Any]:
        """Insert one company_purge_and_copy_logs record for a company."""
        return self._post(
            f'/api/admin/company-purge-and-copy-logs/{coid}',
            json=drop_none({'user': user, 'reason': reason, 'event': event, 'status': status}),
        )
