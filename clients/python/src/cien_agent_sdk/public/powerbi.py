from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class PublicPowerBIAPI(EndpointGroup):
    """/api/powerbi endpoints."""

    def list_workspaces(self) -> list[dict[str, Any]]:
        return self._get("/api/powerbi/workspaces")

    def get_workspace(self, workspace_id: str) -> dict[str, Any]:
        return self._get(f"/api/powerbi/workspaces/{workspace_id}")

    def list_reports(self, workspace_id: str) -> list[dict[str, Any]]:
        return self._get(f"/api/powerbi/workspaces/{workspace_id}/reports")

    def list_report_pages(self, workspace_id: str, report_id: str) -> list[dict[str, Any]]:
        return self._get(f"/api/powerbi/workspaces/{workspace_id}/reports/{report_id}/pages")

    def list_datasets(self, workspace_id: str) -> list[dict[str, Any]]:
        return self._get(f"/api/powerbi/workspaces/{workspace_id}/datasets")

    def generate_embed_token(
        self,
        workspace_id: str,
        report_id: str,
        *,
        dataset_ids: list[str] | None = None,
        access_level: str = "View",
        lifetime_minutes: int | None = None,
        allow_save_as: bool = False,
    ) -> dict[str, Any]:
        return self._post(
            f"/api/powerbi/workspaces/{workspace_id}/reports/{report_id}/embed-token",
            json={
                "dataset_ids": dataset_ids,
                "access_level": access_level,
                "lifetime_minutes": lifetime_minutes,
                "allow_save_as": allow_save_as,
            },
        )
