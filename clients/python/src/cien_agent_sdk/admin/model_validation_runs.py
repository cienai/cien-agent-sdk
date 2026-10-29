from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminModelValidationRunsAPI(EndpointGroup):
    """Validation runs: the exact Model Definition version a run scored and its per-row outcomes."""

    def start(self, *, model_definition_id: str, dag_run_id: str, dag_id: str | None = None,
              llm_model_name: str | None = None, provider: str | None = None) -> dict[str, Any]:
        """Pin the definition version and open (or resume) the run attempt for this DAG run.

        Returns ``run``, the pinned ``definition`` (with ``validation_data`` and ``dataset_revision``) and
        ``completed`` (true when this DAG run already scored the definition successfully).
        """
        return self._post("/api/admin/model-validation-runs", json={
            "model_definition_id": model_definition_id, "dag_run_id": dag_run_id, "dag_id": dag_id,
            "llm_model_name": llm_model_name, "provider": provider,
        })

    def finish(self, run_id: str, *, status: str, outcomes: list[dict[str, Any]] | None = None,
               error_message: str | None = None, llm_model_name: str | None = None,
               provider: str | None = None) -> dict[str, Any]:
        """Record ``success`` with per-row outcomes, or ``failed`` with an error; repeating it is a no-op."""
        return self._post(f"/api/admin/model-validation-runs/{run_id}/finish", json={
            "status": status, "error_message": error_message, "outcomes": outcomes or [],
            "llm_model_name": llm_model_name, "provider": provider,
        })

    def list(self, definition_id: str, *, page: int = 1, page_size: int = 20) -> dict[str, Any]:
        return self._get(f"/api/model-definitions/{definition_id}/validation-runs",
                         params={"page": page, "page_size": page_size})

    def get(self, run_id: str) -> dict[str, Any]:
        return self._get(f"/api/model-definitions/validation-runs/{run_id}")

    def failed_examples(self, run_id: str, *, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        return self._get(f"/api/model-definitions/validation-runs/{run_id}/failed-examples",
                         params={"page": page, "page_size": page_size})

    def compare(self, *, baseline_run_id: str, candidate_run_id: str) -> dict[str, Any]:
        return self._get("/api/model-definitions/validation-runs/compare",
                         params={"baseline_run_id": baseline_run_id, "candidate_run_id": candidate_run_id})
