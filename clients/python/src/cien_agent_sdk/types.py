"""Shared type aliases."""

from __future__ import annotations

from typing import Any
from typing import Any, TypedDict

JSONDict = dict[str, Any]
JSONList = list[JSONDict]


class ResetSyncResponse(TypedDict):
	message: str
	coid: str
	entity: str
	status_cleared: bool
	deleted_files: list[str]
	errors: list[str]
