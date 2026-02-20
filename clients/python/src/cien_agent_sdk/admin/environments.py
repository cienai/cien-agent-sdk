from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminEnvironmentsAPI(EndpointGroup):
    """/api/admin/environments endpoints."""

    def list(self, *, coid: str, include_sync: bool = False) -> dict[str, Any]:
        return self._get("/api/admin/environments", params={"coid": coid, "include_sync": include_sync})

    def get(self, coid: str, *, environment: str = "staging", include_sync: bool = False) -> dict[str, Any]:
        return self._get(
            f"/api/admin/environments/{coid}",
            params={"environment": environment, "include_sync": include_sync},
        )

    def create(self, *, data: dict[str, Any], environment: str = "staging") -> dict[str, Any]:
        return self._post(
            "/api/admin/environments",
            json={"data": data},
            params={"environment": environment},
        )

    def update(
        self,
        coid: str,
        *,
        updates: dict[str, Any],
        environment: str = "staging",
    ) -> dict[str, Any]:
        return self._patch(
            f"/api/admin/environments/{coid}",
            json={"updates": updates},
            params={"environment": environment},
        )

    def delete(self, coid: str, *, environment: str = "staging") -> dict[str, Any]:
        return self._delete(f"/api/admin/environments/{coid}", params={"environment": environment})

    def copy(
        self,
        coid: str,
        *,
        source_environment: str = "prod",
        destination_environment: str = "staging",
        include_sync: bool = True,
        overwrite_sync: bool = True,
    ) -> dict[str, Any]:
        return self._post(
            f"/api/admin/environments/{coid}/copy",
            json=drop_none(
                {
                    "source_environment": source_environment,
                    "destination_environment": destination_environment,
                    "include_sync": include_sync,
                    "overwrite_sync": overwrite_sync,
                }
            ),
        )
