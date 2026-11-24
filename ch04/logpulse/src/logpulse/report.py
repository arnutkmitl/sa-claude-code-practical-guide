"""Turn parsed log entries into a summary."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

from logpulse.parsers import AccessEntry, SyslogEntry

ERROR_WORDS = ("error", "fail", "denied", "timeout")


def summarize_access(
    entries: list[AccessEntry], slow_threshold: float = 1.0, top: int = 5
) -> dict:
    total = len(entries)
    classes = Counter(f"{e.status // 100}xx" for e in entries)
    errors = sum(1 for e in entries if e.status >= 500)

    times: dict[str, list[float]] = defaultdict(list)
    for e in entries:
        times[e.path].append(e.request_time)
    averages = {p: sum(t) / len(t) for p, t in times.items()}
    slow = sorted(
        ((p, a) for p, a in averages.items() if a >= slow_threshold),
        key=lambda item: item[1],
        reverse=True,
    )[:top]

    error_paths = Counter(e.path for e in entries if e.status >= 500)
    return {
        "requests": total,
        "status_classes": dict(sorted(classes.items())),
        "error_rate": round(errors / total, 4) if total else 0.0,
        "slow_endpoints": [
            {"path": p, "avg_seconds": round(a, 3)} for p, a in slow
        ],
        "top_error_paths": error_paths.most_common(top),
    }


def summarize_syslog(entries: list[SyslogEntry], top: int = 5) -> dict:
    programs = Counter(e.program for e in entries)
    problems = [
        e for e in entries
        if any(word in e.message.lower() for word in ERROR_WORDS)
    ]
    return {
        "lines": len(entries),
        "busiest_programs": programs.most_common(top),
        "problem_lines": len(problems),
        "problem_programs": Counter(
            e.program for e in problems
        ).most_common(top),
    }


def format_text(summary: dict) -> str:
    lines: list[str] = []
    if "requests" in summary:
        lines.append(f"Requests:    {summary['requests']}")
        classes = "  ".join(
            f"{k}={v}" for k, v in summary["status_classes"].items()
        )
        lines.append(f"Status:      {classes}")
        lines.append(f"Error rate:  {summary['error_rate']:.2%}")
        lines.append("Slow endpoints (avg seconds):")
        for item in summary["slow_endpoints"]:
            lines.append(f"  {item['avg_seconds']:>6.3f}  {item['path']}")
        lines.append("Top 5xx paths:")
        for path, count in summary["top_error_paths"]:
            lines.append(f"  {count:>6}  {path}")
    else:
        lines.append(f"Lines:          {summary['lines']}")
        lines.append(f"Problem lines:  {summary['problem_lines']}")
        lines.append("Programs with problems:")
        for program, count in summary["problem_programs"]:
            lines.append(f"  {count:>6}  {program}")
    return "\n".join(lines)


def format_json(summary: dict) -> str:
    return json.dumps(summary, indent=2)
