from datetime import datetime

from logpulse.cli import main
from logpulse.parsers import AccessEntry, SyslogEntry, read_syslog
from logpulse.report import summarize_access, summarize_syslog


def make(path, status, rt):
    return AccessEntry(
        "203.0.113.1",
        datetime(2026, 11, 5, 6, 0),
        "GET",
        path,
        status,
        100,
        rt,
    )


def test_summary_counts_and_error_rate():
    entries = [
        make("/a", 200, 0.1),
        make("/a", 500, 0.2),
        make("/b", 404, 0.1),
        make("/b", 200, 0.1),
    ]
    summary = summarize_access(entries)
    assert summary["requests"] == 4
    assert summary["status_classes"] == {"2xx": 2, "4xx": 1, "5xx": 1}
    assert summary["error_rate"] == 0.25


def test_slow_endpoints_sorted_by_average():
    entries = [
        make("/slow", 200, 3.0),
        make("/slower", 200, 5.0),
        make("/fast", 200, 0.1),
    ]
    slow = summarize_access(entries, slow_threshold=1.0)["slow_endpoints"]
    assert [item["path"] for item in slow] == ["/slower", "/slow"]


def test_empty_log_has_zero_error_rate():
    assert summarize_access([])["error_rate"] == 0.0


def test_syslog_problem_lines():
    entries = [
        SyslogEntry("Nov  5 06:00:00", "web01", "sshd", "Failed password"),
        SyslogEntry("Nov  5 06:00:01", "web01", "CRON", "(root) CMD (x)"),
    ]
    summary = summarize_syslog(entries)
    assert summary["problem_lines"] == 1
    assert summary["problem_programs"] == [("sshd", 1)]


def test_syslog_counts_timed_out_and_oom_kill_as_problems(tmp_path):
    log = tmp_path / "syslog.log"
    log.write_text(
        "Nov  5 06:01:34 web01 nginx[6426]: upstream timed out (110: "
        "Connection timed out) while reading response header from "
        "upstream\n"
        "Nov  5 06:18:59 web01 kernel: Out of memory: Killed process "
        "2211 (php-fpm)\n"
        "Nov  5 06:02:33 web01 sshd[6442]: Accepted publickey for deploy "
        "from 203.0.113.20 port 51122\n"
    )
    entries, _ = read_syslog(str(log))
    summary = summarize_syslog(entries)
    assert summary["problem_lines"] == 2
    assert sorted(summary["problem_programs"]) == [("kernel", 1), ("nginx", 1)]


def test_cli_missing_file_returns_2(capsys):
    assert main(["does-not-exist.log"]) == 2
    assert "no such file" in capsys.readouterr().err
