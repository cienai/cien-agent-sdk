from __future__ import annotations

from cien_agent_sdk.utils import drop_none


def test_drop_none_removes_only_none_values() -> None:
    data = {"a": 1, "b": None, "c": False, "d": 0, "e": "", "f": []}

    assert drop_none(data) == {"a": 1, "c": False, "d": 0, "e": "", "f": []}

