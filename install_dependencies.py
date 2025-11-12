"""Install required Python packages for the 4G Node Pulse dashboard."""
from __future__ import annotations

import subprocess
import sys
from typing import List


REQUIRED_PACKAGES: List[str] = [
    "flask>=2.0.0",
]


def main() -> None:
    """Install the dashboard's Python dependencies using pip."""
    if not REQUIRED_PACKAGES:
        return

    command = [sys.executable, "-m", "pip", "install", *REQUIRED_PACKAGES]
    print("Running:", " ".join(command))
    subprocess.check_call(command)


if __name__ == "__main__":
    main()
