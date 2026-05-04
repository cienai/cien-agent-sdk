from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminCopyToStagingLogAPI(EndpointGroup):
    """/api/admin/copy-to-staging-log endpoints."""

    def create(self, coid: str, *, user: str, reason: str = '') -> dict[str, Any]:
        """Insert one copy_to_staging_log record for a company."""
        return self._post(
            f'/api/admin/copy-to-staging-log/{coid}',
            json=drop_none({'user': user, 'reason': reason}),
        )
