"""PreToolUse hook: block recursive deletes and force pushes."""

import json
import re
import shlex
import sys

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")


def words(part: str) -> list[str]:
    try:
        return shlex.split(part)
    except ValueError:
        return part.split()


def blocked(part: str) -> str | None:
    w = words(part)
    if not w:
        return None
    if w[0] == "rm":
        flags = "".join(x.lstrip("-") for x in w[1:] if x.startswith("-"))
        if "r" in flags.lower() and "f" in flags:
            return "recursive forced delete (rm -rf)"
    if w[:2] == ["git", "push"]:
        if any(x in ("--force", "-f") or x.startswith("--force=")
               for x in w[2:]):
            return "force push (use --force-with-lease after review)"
    return None


# Check every part of a compound command, as permission rules do.
for part in re.split(r"&&|\|\||;|\||&|\n", command):
    reason = blocked(part.strip())
    if reason:
        print(f"Blocked by guard_bash.py: {reason}. Ask the user "
              "to run it themselves if it is really needed.",
              file=sys.stderr)
        sys.exit(2)
sys.exit(0)
