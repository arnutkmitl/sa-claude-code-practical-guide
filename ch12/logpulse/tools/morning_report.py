"""Write a short morning summary of yesterday's logs with Claude Code.

Usage: python tools/morning_report.py ACCESS_LOG SYSLOG [OUT_DIR]

Runs logpulse on both logs, asks Claude for a structured verdict, and
writes OUT_DIR/YYYY-MM-DD.md. Exits 1 when the verdict is "alert", so
cron or CI can notify someone.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok", "warn", "alert"]},
        "headline": {"type": "string"},
        "findings": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["status", "headline", "findings"],
}

PROMPT = """You are the on-call engineer's assistant. Below are two
logpulse JSON reports for one web server: the nginx access log and
the syslog. Decide whether a human needs to act this morning.

Use "alert" for an error rate above 5% or kernel out-of-memory kills,
"warn" for slow endpoints above 2 seconds or repeated failed logins,
and "ok" otherwise. Give a one-sentence headline and at most five
findings, each with the number that supports it. Use only the data
below; do not guess about causes you can't see.
"""


def logpulse_json(path: str, log_type: str) -> dict:
    out = subprocess.run(
        ["logpulse", path, "--type", log_type, "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def ask_claude(reports: dict) -> dict:
    # fmt: off
    cmd = [
        "claude", "-p", PROMPT,
        "--tools", "",                  # no tools: read the input only
        "--permission-mode", "dontAsk",
        "--max-budget-usd", "0.50",
        "--output-format", "json",
        "--json-schema", json.dumps(SCHEMA),
    ]
    # fmt: on
    out = subprocess.run(
        cmd,
        input=json.dumps(reports, indent=2),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if out.returncode != 0:
        raise SystemExit(f"morning_report: claude failed: {out.stderr}")
    result = json.loads(out.stdout)
    if result.get("is_error"):
        raise SystemExit(f"morning_report: {result.get('result')}")
    verdict = result["structured_output"]
    verdict["cost_usd"] = result.get("total_cost_usd")
    return verdict


def main(access_log: str, syslog: str, out_dir: str = "reports") -> int:
    reports = {
        "access": logpulse_json(access_log, "access"),
        "syslog": logpulse_json(syslog, "syslog"),
    }
    verdict = ask_claude(reports)
    lines = [
        f"# Morning report {date.today().isoformat()}",
        "",
        f"Status: {verdict['status'].upper()}",
        "",
        verdict["headline"],
        "",
        *[f"- {item}" for item in verdict["findings"]],
        "",
        f"(Claude cost: USD {verdict['cost_usd']})",
    ]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"{date.today().isoformat()}.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{verdict['status']}: {verdict['headline']} -> {target}")
    return 1 if verdict["status"] == "alert" else 0


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print(__doc__.strip(), file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(*sys.argv[1:]))
