"""Flask application for the 4G Node Pulse Dashboard."""
from __future__ import annotations

import datetime
from typing import Dict, List

from flask import Flask, jsonify, render_template

from service_checks import (
    check_cell_transmit_state,
    check_enodeb_status,
    check_mesh_radio_status,
    check_transmit_parameters,
    check_vpn_vm_status,
)

app = Flask(__name__)

# Node configuration. Add or remove entries to update the dashboard automatically.
NODES: List[Dict[str, str]] = [
    {"name": "Node Alpha", "ip": "192.168.10.2"},
    {"name": "Node Bravo", "ip": "192.168.20.2"},
    {"name": "Node Charlie", "ip": "192.168.30.2"},
]


def _compute_overall_status(statuses: List[str]) -> str:
    """Return aggregate status for a node based on individual checks."""
    if any(status == "FAIL" for status in statuses):
        return "FAIL"
    if any(status == "WARN" for status in statuses):
        return "WARN"
    return "OK"


def gather_node_status(node: Dict[str, str]) -> Dict[str, object]:
    """Collect all service check results for the provided node."""
    enodeb = check_enodeb_status(node)
    transmit_params = check_transmit_parameters(node)
    mesh_radio = check_mesh_radio_status(node)
    vpn_vm = check_vpn_vm_status(node)
    cell1 = check_cell_transmit_state(node, 1)
    cell2 = check_cell_transmit_state(node, 2)

    statuses = [
        enodeb["status"],
        transmit_params["status"],
        mesh_radio["status"],
        vpn_vm["status"],
        cell1["status"],
        cell2["status"],
    ]

    return {
        "name": node["name"],
        "ip": node["ip"],
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "overall_status": _compute_overall_status(statuses),
        "services": {
            "eNodeB": enodeb,
            "Transmit Parameters": transmit_params,
            "Mesh Radio (MPU5)": mesh_radio,
            "VPN VM": vpn_vm,
            "Cell 1": cell1,
            "Cell 2": cell2,
        },
    }


def _node_index_by_name(name: str) -> int:
    for index, node in enumerate(NODES):
        if node["name"].lower() == name.lower():
            return index
    raise ValueError(f"Node '{name}' not found")


@app.route("/")
def dashboard() -> str:
    node_statuses = [gather_node_status(node) for node in NODES]
    node_statuses.sort(key=lambda entry: entry["name"].lower())
    return render_template("index.html", nodes=node_statuses)


@app.route("/api/nodes")
def api_nodes():
    node_statuses = [gather_node_status(node) for node in NODES]
    node_statuses.sort(key=lambda entry: entry["name"].lower())
    summaries = [
        {
            "name": node["name"],
            "ip": node["ip"],
            "overall_status": node["overall_status"],
            "checked_at": node["checked_at"],
        }
        for node in node_statuses
    ]
    return jsonify({"nodes": summaries})


@app.route("/api/node/<name>")
def api_node_detail(name: str):
    try:
        node = NODES[_node_index_by_name(name)]
    except ValueError:
        return jsonify({"error": "Node not found"}), 404

    node_status = gather_node_status(node)
    return jsonify(node_status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
