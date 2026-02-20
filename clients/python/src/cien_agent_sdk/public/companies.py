from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class PublicCompaniesAPI(EndpointGroup):
    """/api/companies endpoints."""

    def list(
        self,
        *,
        selected_columns: list[str] | None = None,
        filters: str | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        natural_query: str | None = None,
    ) -> list[dict[str, Any]]:
        """List companies using query-string filters."""
        return self._get(
            "/api/companies",
            params=drop_none(
                {
                    "selected_columns": selected_columns,
                    "filters": filters,
                    "order_by": order_by,
                    "limit": limit,
                    "natural_query": natural_query,
                }
            ),
        )

    def search(
        self,
        *,
        selected_columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        natural_query: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search companies using a structured JSON payload."""
        payload = drop_none(
            {
                "selected_columns": selected_columns,
                "filters": filters,
                "order_by": order_by,
                "limit": limit,
                "natural_query": natural_query,
            }
        )
        return self._post("/api/companies/search", json=payload)

    def get(self, coid: str, *, selected_columns: list[str] | None = None) -> dict[str, Any]:
        """Fetch one company by COID."""
        return self._get(
            "/api/companies/companies",
            params=drop_none({"coid": coid, "selected_columns": selected_columns}),
        )

    def lookup(
        self,
        *,
        company_id: str | None = None,
        company_name: str | None = None,
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Look up one company by ID or name."""
        return self._get(
            "/api/companies/lookup",
            params=drop_none(
                {
                    "company_id": company_id,
                    "company_name": company_name,
                    "selected_columns": selected_columns,
                }
            ),
        )

    def update(
        self,
        company_id: str,
        *,
        updates: dict[str, Any],
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Apply partial field updates to one company."""
        return self._patch(
            f"/api/companies/{company_id}",
            json={"updates": updates, "selected_columns": selected_columns},
        )

    def delete(self, company_id: str) -> dict[str, Any]:
        """Delete one company by internal company ID."""
        return self._delete(f"/api/companies/{company_id}")
