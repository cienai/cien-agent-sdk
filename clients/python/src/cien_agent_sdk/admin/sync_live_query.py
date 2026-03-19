from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminSyncLiveQueryAPI(EndpointGroup):
    """/api/admin/sync_live_query endpoints."""

    def describe(
        self,
        *,
        coid: str,
        crm_entity: str,
        column_names_only: bool = False,
    ) -> Any:
        """Describe one CRM entity for a company's current sync."""
        return self._post(
            "/api/admin/sync_live_query/describe",
            json={
                "coid": coid,
                "crm_entity": crm_entity,
                "column_names_only": column_names_only,
            },
        )

    def query(
        self,
        *,
        coid: str,
        crm_entity: str,
        query: str,
        limit: int | str | None = None,
    ) -> Any:
        """Run one live CRM query for a company's current sync."""
        return self._post(
            "/api/admin/sync_live_query/query",
            json=drop_none(
                {
                    "coid": coid,
                    "crm_entity": crm_entity,
                    "query": query,
                    "limit": limit,
                }
            ),
        )
