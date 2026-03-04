from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..errors import APIError
from ..utils import drop_none


class AdminSyncAPI(EndpointGroup):
    """/api/admin/sync endpoints."""

    def list(
        self,
        *,
        coid: str | None = None,
        sync_token: str | None = None,
        sync_type: str | None = None,
        is_active: bool | None = None,
    ) -> list[dict[str, Any]]:
        """List sync records filtered by company id and/or sync token."""
        if not coid and not sync_token:
            raise ValueError("Either coid or sync_token is required")
        return self._get(
            "/api/admin/sync",
            params=drop_none(
                {
                    "coid": coid,
                    "sync_token": sync_token,
                    "sync_type": sync_type,
                    "_sys_isactive": is_active,
                }
            ),
        )

    def get_by_sync_token(self, sync_token: str) -> dict[str, Any] | None:
        """Fetch one sync record by sync token, or None if not found."""
        try:
            return self._get(f"/api/admin/sync/by-token/{sync_token}")
        except APIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def get(self, sync_id: int) -> dict[str, Any]:
        """Fetch one sync record by ID."""
        return self._get(f"/api/admin/sync/{sync_id}")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a sync record from the provided payload."""
        return self._post("/api/admin/sync", json=payload)

    def update(self, sync_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """Update an existing sync record."""
        return self._patch(f"/api/admin/sync/{sync_id}", json=payload)

    def delete(self, sync_id: int) -> None:
        """Delete a sync record by ID."""
        self._delete(f"/api/admin/sync/{sync_id}")
