"""Command-line interface for logpulse."""

from __future__ import annotations

import argparse
import sys

from logpulse import __version__
from logpulse.parsers import read_access_log, read_syslog
from logpulse.report import (
    format_json,
    format_text,
    summarize_access,
    summarize_syslog,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logpulse",
        description="Summarize an nginx access log or a syslog file.",
    )
    parser.add_argument("logfile", help="path to the log file")
    parser.add_argument(
        "--type", choices=["access", "syslog"], default="access",
        help="log format (default: access)",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="output format (default: text)",
    )
    parser.add_argument(
        "--slow-threshold", type=float, default=1.0, metavar="SECONDS",
        help="average request time that counts as slow (default: 1.0)",
    )
    parser.add_argument(
        "--version", action="version", version=f"logpulse {__version__}"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.type == "access":
            entries, skipped = read_access_log(args.logfile)
            summary = summarize_access(entries, args.slow_threshold)
        else:
            entries, skipped = read_syslog(args.logfile)
            summary = summarize_syslog(entries)
    except FileNotFoundError:
        print(f"logpulse: no such file: {args.logfile}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(format_json(summary))
    else:
        print(format_text(summary))
    if skipped:
        print(f"logpulse: skipped {skipped} unparsed line(s)",
              file=sys.stderr)
    return 0
