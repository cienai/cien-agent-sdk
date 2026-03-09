from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminCrmAPI(EndpointGroup):
    """/api/admin/crm endpoints."""

    def describe(self, *, coid: str, table: str, column_names_only: bool = False) -> Any:
        """Describe one CRM table for a company's current sync."""
        return self._post(
            "/api/admin/crm/describe",
            json={
                "coid": coid,
                "table": table,
                "column_names_only": column_names_only,
            },
        )

    def query(self, *, coid: str, table: str, query: str, limit: int | None = None) -> Any:
        """Run one CRM query for a company's current sync."""
        return self._post(
            "/api/admin/crm/query",
            json={
                "coid": coid,
                "table": table,
                "query": query,
                "limit": limit,
            },
        )
