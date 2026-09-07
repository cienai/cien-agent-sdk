from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminJobsAPI(EndpointGroup):
    """/api/admin/jobs endpoints."""

    def run(self, *, coid: str, job_type: str, processing_mode: str | None = None, priority: bool = False) -> dict[str, Any]:
        """Trigger a job for one company."""
        return self._post(
            "/api/admin/jobs/run",
            json={
                "coid": coid,
                "jobType": job_type,
                **({"processingMode": processing_mode} if processing_mode is not None else {}),
                "priority": priority,
            },
        )

    def list(self, coid: str, *, limit: int | None = None) -> list[dict[str, Any]]:
        """List jobs for one company."""
        params = {"limit": limit} if limit is not None else None
        return self._get(f"/api/admin/jobs/{coid}", params=params)

    def cancel(self, *, coid: str, dag_run_id: str) -> dict[str, Any]:
        """Cancel one dag run for one company."""
        return self._post(f"/api/admin/jobs/{coid}/{dag_run_id}/cancel")
