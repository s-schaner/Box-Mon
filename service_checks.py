"""Service check functions for 4G node monitoring dashboard."""
from __future__ import annotations

import random
from typing import Dict, Literal

Status = Literal["OK", "WARN", "FAIL"]

_STATUS_CHOICES = [
    ("OK", ["Operating within expected parameters.", "No issues detected.", "Systems nominal."]),
    ("WARN", [
        "Minor inconsistencies detected; monitor conditions.",
        "Performance degradation observed; investigate soon.",
        "Potential configuration drift identified.",
    ]),
    ("FAIL", [
        "Critical fault detected; service unavailable.",
        "Hardware fault reported; immediate action required.",
        "Service offline due to connectivity loss.",
    ]),
]


def _random_status() -> Dict[str, str]:
    """Return a random status payload to simulate a service check."""
    status, details_pool = random.choice(_STATUS_CHOICES)
    return {"status": status, "details": random.choice(details_pool)}


def check_enodeb_status(node: Dict[str, str]) -> Dict[str, str]:
    """Mock check for the eNodeB operational status."""
    result = _random_status()
    if result["status"] == "OK":
        result["details"] = f"eNodeB for {node['name']} responding normally."
    return result


def check_transmit_parameters(node: Dict[str, str]) -> Dict[str, str]:
    """Mock check for LTE broadcast parameters (SIB/MIB/PLMN)."""
    result = _random_status()
    if result["status"] == "OK":
        result["details"] = "SIB/MIB/PLMN parameters validated."
    return result


def check_mesh_radio_status(node: Dict[str, str]) -> Dict[str, str]:
    """Mock check for integrated mesh radio (MPU5) status."""
    result = _random_status()
    if result["status"] == "OK":
        result["details"] = "MPU5 mesh network link stable."
    return result


def check_vpn_vm_status(node: Dict[str, str]) -> Dict[str, str]:
    """Mock check for VPN virtual machine status."""
    result = _random_status()
    if result["status"] == "OK":
        result["details"] = "VPN VM reachable and authenticated."
    return result


def check_cell_transmit_state(node: Dict[str, str], cell_id: int) -> Dict[str, str]:
    """Mock check for the transmit/lock state of a specific cell."""
    result = _random_status()
    if result["status"] == "OK":
        result["details"] = f"Cell {cell_id} transmitting without alarms."
    return result
