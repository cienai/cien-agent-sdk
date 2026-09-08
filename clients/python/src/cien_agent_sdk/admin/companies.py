from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

from ..base import EndpointGroup
from ..utils import drop_none


class CompanyCreateData(BaseModel):
    partner_id: str
    name: str
    region: Literal["us", "eu"]


class AdminCompaniesAPI(EndpointGroup):
    """/api/admin/companies endpoints."""

    def list(
        self,
        *,
        selected_columns: list[str] | None = None,
        filters: str | None = None,
        order_by: str | None = None,
        limit: int | None = None
    ) -> list[dict[str, Any]]:
        """List companies with admin-only filters for partner and org scope."""
        return self._get(
            "/api/admin/companies",
            params=drop_none(
                {
                    "selected_columns": selected_columns,
                    "filters": filters,
                    "order_by": order_by,
                    "limit": limit
                }
            ),
        )

    def search(
        self,
        *,
        selected_columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None
    ) -> list[dict[str, Any]]:
        """Search companies with admin-only filters using a JSON payload."""
        payload = drop_none(
            {
                "selected_columns": selected_columns,
                "filters": filters,
                "order_by": order_by,
                "limit": limit
            }
        )
        return self._post("/api/admin/companies/search", json=payload)

    def create(
        self,
        *,
        data: CompanyCreateData,
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create one company through the admin API."""
        return self._post(
            "/api/admin/companies",
            json={"data": data.model_dump(), "selected_columns": selected_columns},
        )

    def get(self, coid: str, *, selected_columns: list[str] | None = None) -> dict[str, Any]:
        """Fetch one company record by COID through admin APIs (cached briefly)."""
        columns_key = tuple(selected_columns) if selected_columns is not None else None
        return self._get_cached(
            "/api/admin/companies/companies",
            params=drop_none({"coid": coid, "selected_columns": selected_columns}),
            cache_key=("companies", coid, "get", columns_key),
            ttl=450,
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
        result = self._patch(
            f"/api/admin/companies/{company_id}",
            json={"updates": updates, "selected_columns": selected_columns},
        )
        self._invalidate_cache(("companies", company_id))
        return result

    def delete(self, company_id: str) -> dict[str, Any]:
        """Delete one company by internal company ID via admin endpoint."""
        result = self._delete(f"/api/admin/companies/{company_id}")
        self._invalidate_cache(("companies", company_id))
        return result
