from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminJobEngineLogsAPI(EndpointGroup):
    """/api/admin/job-engine-logs endpoints."""

    def save(
        self,
        coid: str,
        *,
        dag_log: dict[str, Any],
        task_logs: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Upsert one DAG log and its task logs for a company."""
        return self._patch(
            f'/api/admin/job-engine-logs/{coid}',
            json=drop_none({'dag_log': dag_log, 'task_logs': task_logs or []}),
        )
