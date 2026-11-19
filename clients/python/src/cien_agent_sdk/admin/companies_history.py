from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminCompaniesHistoryAPI(EndpointGroup):
    """/api/admin/companies-history endpoints."""

    def get(self, coid: str, *, selected_columns: list[str] | None = None) -> dict[str, Any] | None:
        """Fetch the latest companies_history row for a company."""
        return self._get(
            f"/api/admin/companies-history/{coid}",
            params=drop_none({"selected_columns": selected_columns}),
        )

    def get_for_export(self, coid: str, *, dag_run_id: str | None = None, selected_columns: list[str] | None = None) -> dict[str, Any] | None:
        """Fetch the current run's row, or the latest row when no run is supplied.

        Unlike :meth:`get`, a coid with no successful run yet still gets its latest row.
        """
        return self._get(
            f"/api/admin/companies-history/{coid}/export",
            params=drop_none({"dag_run_id": dag_run_id, "selected_columns": selected_columns}),
        )

    def save(
        self,
        coid: str,
        dag_run_id: str,
        *,
        updates: dict[str, Any],
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        """Upsert a companies_history row keyed by dag_run_id.

        If a row for this coid + dag_run_id already exists it is updated;
        otherwise a new row is inserted.
        """
        return self._patch(
            f"/api/admin/companies-history/{coid}",
            json=drop_none(
                {
                    "dag_run_id": dag_run_id,
                    "updates": updates,
                    "selected_columns": selected_columns,
                }
            ),
        )

    def update(
        self,
        coid: str,
        dag_run_id: str,
        *,
        updates: dict[str, Any],
        selected_columns: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Update an existing companies_history row when it exists.

        Returns ``None`` when the row does not exist.
        """
        return self._patch(
            f"/api/admin/companies-history/{coid}/{dag_run_id}",
            json=drop_none(
                {
                    "updates": updates,
                    "selected_columns": selected_columns,
                }
            ),
        )
