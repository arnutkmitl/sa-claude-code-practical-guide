from datetime import datetime

from logpulse.parsers import (
    parse_access_line,
    parse_syslog_line,
    read_access_log,
)

ACCESS = (
    '203.0.113.16 - - [05/Nov/2026:06:00:45 +0700] '
    '"GET /api/search?q=disk HTTP/1.1" 200 512 "-" "curl/8.5.0" 1.250'
)


def test_access_line_fields():
    entry = parse_access_line(ACCESS)
    assert entry is not None
    assert entry.ip == "203.0.113.16"
    assert entry.method == "GET"
    assert entry.path == "/api/search"
    assert entry.status == 200
    assert entry.size == 512
    assert entry.request_time == 1.25


def test_access_time_date_and_clock():
    entry = parse_access_line(ACCESS)
    assert entry.time.date() == datetime(2026, 11, 5).date()
    assert entry.time.hour == 6


def test_access_dash_size_is_zero():
    line = ACCESS.replace(" 200 512 ", " 304 - ")
    assert parse_access_line(line).size == 0


def test_access_garbage_returns_none():
    assert parse_access_line("not a log line") is None


def test_access_impossible_date_is_skipped(tmp_path):
    bad = ACCESS.replace("05/Nov/2026", "31/Nov/2026")
    log = tmp_path / "access.log"
    log.write_text(ACCESS + "\n" + bad + "\n", encoding="utf-8")
    entries, skipped = read_access_log(str(log))
    assert len(entries) == 1
    assert skipped == 1


def test_syslog_line_with_pid():
    entry = parse_syslog_line(
        "Nov  5 06:01:34 web01 sshd[812]: Failed password for root"
    )
    assert entry.program == "sshd"
    assert entry.host == "web01"
    assert entry.message.startswith("Failed password")


def test_syslog_line_without_pid():
    entry = parse_syslog_line(
        "Nov  5 06:00:34 web01 kernel: EXT4-fs (sda1): mounted filesystem"
    )
    assert entry.program == "kernel"
