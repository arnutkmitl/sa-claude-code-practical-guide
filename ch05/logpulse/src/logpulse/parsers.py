"""Parsers for nginx access logs and syslog lines."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

# nginx "combined" format with $request_time appended at the end.
ACCESS_RE = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+|-) '
    r'"[^"]*" "[^"]*" (?P<rt>[\d.]+)'
)

SYSLOG_RE = re.compile(
    r"(?P<ts>\w{3} [ \d]\d \d\d:\d\d:\d\d) (?P<host>\S+) "
    r"(?P<program>[\w./-]+)(?:\[\d+\])?: (?P<message>.*)"
)


@dataclass
class AccessEntry:
    ip: str
    time: datetime
    method: str
    path: str
    status: int
    size: int
    request_time: float


@dataclass
class SyslogEntry:
    time_text: str
    host: str
    program: str
    message: str


def parse_access_time(text: str) -> datetime:
    """Parse an nginx time such as 05/Nov/2026:08:15:02 +0700."""
    stamp = text.split(" ")[0]
    return datetime.strptime(stamp, "%d/%b/%Y:%H:%M:%S")


def parse_access_line(line: str) -> AccessEntry | None:
    match = ACCESS_RE.match(line)
    if match is None:
        return None
    size = match["size"]
    return AccessEntry(
        ip=match["ip"],
        time=parse_access_time(match["ts"]),
        method=match["method"],
        path=match["path"].split("?")[0],
        status=int(match["status"]),
        size=0 if size == "-" else int(size),
        request_time=float(match["rt"]),
    )


def parse_syslog_line(line: str) -> SyslogEntry | None:
    match = SYSLOG_RE.match(line)
    if match is None:
        return None
    return SyslogEntry(
        time_text=match["ts"],
        host=match["host"],
        program=match["program"],
        message=match["message"],
    )


def read_access_log(path: str) -> tuple[list[AccessEntry], int]:
    """Return parsed entries and the number of lines that did not parse."""
    entries: list[AccessEntry] = []
    skipped = 0
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            entry = parse_access_line(line)
            if entry is None:
                skipped += 1
            else:
                entries.append(entry)
    return entries, skipped


def read_syslog(path: str) -> tuple[list[SyslogEntry], int]:
    entries: list[SyslogEntry] = []
    skipped = 0
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            entry = parse_syslog_line(line)
            if entry is None:
                skipped += 1
            else:
                entries.append(entry)
    return entries, skipped
