from __future__ import annotations

from typing import Any
from ..types import ResetSyncResponse

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
        """List sync records filtered by company id and/or sync token (cached briefly)."""
        if not coid and not sync_token:
            raise ValueError("Either coid or sync_token is required")
        return self._get_cached(
            "/api/admin/sync",
            params=drop_none(
                {
                    "coid": coid,
                    "sync_token": sync_token,
                    "sync_type": sync_type,
                    "_sys_isactive": is_active,
                }
            ),
            cache_key=("sync_list", coid, sync_token, sync_type, is_active),
            ttl=450,
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
        """Fetch one sync record by ID (cached briefly)."""
        return self._get_cached(
            f"/api/admin/sync/{sync_id}",
            cache_key=("sync", sync_id, "get"),
            ttl=450,
        )

    def resolve_box_access_token(self, sync_id: int, *, folder_id: str | None = None) -> str:
        """Resolve a Box access token for this sync's source folder.

        AgentOS mints the token for Cien's shared Box user and verifies it can
        read the sync's configured folder, or `folder_id` when given (to check a
        folder before it replaces the configured one). Tokens last about an hour,
        so this response is intentionally not cached.
        """
        result = self._post(
            f"/api/admin/sync/{sync_id}/box-access-token",
            json={"folder_id": folder_id} if folder_id else None,
        )
        token = str(result.get("access_token") or "").strip()
        if not token:
            raise ValueError("Box access token response was empty")
        return token

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a sync record from the provided payload."""
        result = self._post("/api/admin/sync", json=payload)
        self._invalidate_cache(("sync_list",))
        return result

    def update(self, sync_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """Update an existing sync record."""
        result = self._patch(f"/api/admin/sync/{sync_id}", json=payload)
        self._invalidate_cache(("sync", sync_id))
        self._invalidate_cache(("sync_list",))
        return result

    def delete(self, sync_id: int) -> None:
        """Delete a sync record by ID."""
        self._delete(f"/api/admin/sync/{sync_id}")
        self._invalidate_cache(("sync", sync_id))
        self._invalidate_cache(("sync_list",))

    def reset(self, *, sync_id: int, crm_entity: str, reset_delta: bool = True) -> ResetSyncResponse:
        """Reset sync state for one CRM entity using a sync record id."""
        result = self._post(
            "/api/admin/sync/reset",
            json={
                "sync_id": sync_id,
                "crm_entity": crm_entity,
                "reset_delta": reset_delta,
            },
        )
        self._invalidate_cache(("sync", sync_id))
        self._invalidate_cache(("sync_list",))
        return result
