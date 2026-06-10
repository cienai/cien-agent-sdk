from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminDataDeletionsAPI(EndpointGroup):
    """/api/admin/data-deletions endpoints."""

    def list_pending(self) -> list[dict[str, Any]]:
        """List companies that are marked for deletion and not yet purged."""
        return self._get("/api/admin/data-deletions/pending")
