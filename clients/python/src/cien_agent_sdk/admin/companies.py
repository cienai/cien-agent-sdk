from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminCompaniesAPI(EndpointGroup):
    """/api/admin/companies endpoints."""

    def list(
        self,
        *,
        partner_id: str | None = None,
        clerk_org_id: str | None = None,
        selected_columns: list[str] | None = None,
        filters: str | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        natural_query: str | None = None,
    ) -> list[dict[str, Any]]:
        """List companies with admin-only filters for partner and org scope."""
        return self._get(
            "/api/admin/companies",
            params=drop_none(
                {
                    "partner_id": partner_id,
                    "clerk_org_id": clerk_org_id,
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
        partner_id: str | None = None,
        clerk_org_id: str | None = None,
        selected_columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        natural_query: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search companies with admin-only filters using a JSON payload."""
        payload = drop_none(
            {
                "partner_id": partner_id,
                "clerk_org_id": clerk_org_id,
                "selected_columns": selected_columns,
                "filters": filters,
                "order_by": order_by,
                "limit": limit,
                "natural_query": natural_query,
            }
        )
        return self._post("/api/admin/companies/search", json=payload)

    def get(self, coid: str, *, selected_columns: list[str] | None = None) -> dict[str, Any]:
        """Fetch one company record by COID through admin APIs."""
        return self._get(
            "/api/admin/companies/companies",
            params=drop_none({"coid": coid, "selected_columns": selected_columns}),
        )

    def lookup(
        self,
        *,
        company_id: str | None = None,
        company_name: str | None = None,
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Look up one company by company ID or company name."""
        return self._get(
            "/api/admin/companies/lookup",
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
        """Apply partial updates to one company via admin endpoint."""
        return self._patch(
            f"/api/admin/companies/{company_id}",
            json={"updates": updates, "selected_columns": selected_columns},
        )

    def delete(self, company_id: str) -> dict[str, Any]:
        """Delete one company by internal company ID via admin endpoint."""
        return self._delete(f"/api/admin/companies/{company_id}")
