"""PostToolUse hook: run ruff format on a Python file Claude edited."""

import json
import subprocess
import sys

event = json.load(sys.stdin)
path = event.get("tool_input", {}).get("file_path", "")

if path.endswith(".py"):
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--quiet", path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Not a blocking error: tell Claude, but let the session go on.
        print(f"ruff format failed on {path}:\n{result.stderr}",
              file=sys.stderr)
        sys.exit(1)
sys.exit(0)
