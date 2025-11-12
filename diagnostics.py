"""CLI helper to run mock service checks without starting the web UI."""
from __future__ import annotations

import json
from typing import Any, Dict, Mapping

from app import NODES, gather_node_status

NodeStatus = Mapping[str, Any]
ServiceStatus = Mapping[str, Any]


def format_status(status: NodeStatus) -> str:
    """Return a pretty string for a node status payload."""
    services: Mapping[str, ServiceStatus] = status["services"]
    lines = [
        f"Node: {status['name']} ({status['ip']})",
        f"  Overall: {status['overall_status']} @ {status['checked_at']}",
    ]
    for service_name, payload in services.items():
        lines.append(f"  - {service_name}: {payload['status']} — {payload['details']}")
    return "\n".join(lines)


def main() -> None:
    """Print node status snapshots for all configured nodes."""
    print("Running mock diagnostics...\n")
    for node in NODES:
        snapshot = gather_node_status(node)
        print(format_status(snapshot))
        print("\n---\n")

    print("JSON payload for first node:\n")
    first_snapshot: Dict[str, Any] = gather_node_status(NODES[0])
    print(json.dumps(first_snapshot, indent=2))


if __name__ == "__main__":
    main()
