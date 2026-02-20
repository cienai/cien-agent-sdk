#!/usr/bin/env python3
"""Generate an endpoint catalog from cien-agent-os route files.

This keeps SDK maintenance simple when routes change.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROUTER_RE = re.compile(r"^(?P<name>\w+)\s*=\s*APIRouter\(.*?prefix=\"(?P<prefix>[^\"]*)\"")
DECORATOR_RE = re.compile(
    r"^@(?P<router>\w+)\.(?P<method>get|post|patch|put|delete)\(\"(?P<path>[^\"]*)\""
)

EXCLUDED_PATTERNS = (
    "/api/agentic-definitions",
    "/sessions",
    "/memories",
    "/memory",
    "/memory_topics",
    "/user_memory_stats",
)


@dataclass
class Endpoint:
    method: str
    path: str
    router_name: str
    router_prefix: str
    source_file: str
    source_line: int
    included_in_sdk: bool
    reason: str | None


def normalize_path(prefix: str, route_path: str) -> str:
    base = (prefix or "").strip()
    route = (route_path or "").strip()
    if route in {"", "/"}:
        return base or "/"
    if not base:
        return route if route.startswith("/") else f"/{route}"
    if base.endswith("/"):
        base = base[:-1]
    if route.startswith("/"):
        return f"{base}{route}"
    return f"{base}/{route}"


def include_in_sdk(path: str) -> tuple[bool, str | None]:
    for pattern in EXCLUDED_PATTERNS:
        if path.startswith(pattern):
            return False, f"Excluded pattern: {pattern}"
    return True, None


def parse_file(file_path: Path, root: Path) -> list[Endpoint]:
    router_prefixes: dict[str, str] = {}
    endpoints: list[Endpoint] = []

    lines = file_path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        router_match = ROUTER_RE.match(stripped)
        if router_match:
            router_prefixes[router_match.group("name")] = router_match.group("prefix")
            continue

        decorator_match = DECORATOR_RE.match(stripped)
        if not decorator_match:
            continue

        router_name = decorator_match.group("router")
        method = decorator_match.group("method").upper()
        route_path = decorator_match.group("path")
        prefix = router_prefixes.get(router_name, "")
        full_path = normalize_path(prefix, route_path)
        included, reason = include_in_sdk(full_path)

        endpoints.append(
            Endpoint(
                method=method,
                path=full_path,
                router_name=router_name,
                router_prefix=prefix,
                source_file=str(file_path.relative_to(root)),
                source_line=idx,
                included_in_sdk=included,
                reason=reason,
            )
        )

    return endpoints


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate endpoint catalog from cien-agent-os routes")
    parser.add_argument("--agent-os-path", required=True, help="Path to cien-agent-os directory")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    agent_os_path = Path(args.agent_os_path).resolve()
    routes_path = agent_os_path / "api" / "routes"
    if not routes_path.exists():
        raise SystemExit(f"Route path not found: {routes_path}")

    route_files = sorted(list((routes_path / "public").glob("*.py")) + list((routes_path / "admin").glob("*.py")) + [routes_path / "agentic_definitions.py"])

    all_endpoints: list[Endpoint] = []
    for file_path in route_files:
        if file_path.exists():
            all_endpoints.extend(parse_file(file_path, agent_os_path))

    all_endpoints.sort(key=lambda e: (e.path, e.method))

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "agent_os_path": str(agent_os_path),
        "endpoint_count": len(all_endpoints),
        "sdk_included_count": sum(1 for e in all_endpoints if e.included_in_sdk),
        "endpoints": [asdict(endpoint) for endpoint in all_endpoints],
    }

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_endpoints)} endpoints to {output_path}")


if __name__ == "__main__":
    main()
