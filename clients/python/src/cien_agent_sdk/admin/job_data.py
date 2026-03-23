from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminJobDataAPI(EndpointGroup):
    """/api/admin/job-data endpoints."""

    def get(self, *, coid: str) -> dict[str, Any]:
        """Get the current job_data_conn config for one company."""
        return self._get(f"/api/admin/job-data/{coid}")

    def create(self, *, coid: str) -> dict[str, Any]:
        """Provision a new job_data_conn for one company."""
        return self._post(f"/api/admin/job-data/{coid}/create")

    def save(self, *, coid: str, value: Any, config_type: str | None = None) -> dict[str, Any]:
        """Persist job_data_conn config directly."""
        payload = {"value": value}
        if config_type is not None:
            payload["type"] = config_type
        return self._post(f"/api/admin/job-data/{coid}", json=payload)

    def refresh(self, *, coid: str, region: str) -> dict[str, Any]:
        """Refresh job_data_conn credentials or provision a new container."""
        return self._post(
            f"/api/admin/job-data/{coid}/refresh",
            json=drop_none({"region": region}),
        )

    def explore(
        self,
        *,
        coid: str,
        prefix: str | None = None,
        limit: int | None = None,
        recursive: bool | None = None,
    ) -> dict[str, Any]:
        """List job data paths for one company."""
        return self._get(
            f"/api/admin/job-data/{coid}/explore",
            params=drop_none(
                {
                    "prefix": prefix,
                    "limit": limit,
                    "recursive": recursive,
                }
            ),
        )

    def sizes(
        self,
        *,
        coid: str,
        prefix: str | None = None,
        include_container_total: bool | None = None,
    ) -> dict[str, Any]:
        """Get aggregated immediate-child sizes plus optional container total."""
        return self._get(
            f"/api/admin/job-data/{coid}/sizes",
            params=drop_none(
                {
                    "prefix": prefix,
                    "include_container_total": include_container_total,
                }
            ),
        )
