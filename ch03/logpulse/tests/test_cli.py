import pytest

from logpulse.cli import main

SAMPLE = "samples/access.log"


def test_since_filters_earlier_entries(capsys):
    assert main([SAMPLE, "--format", "json", "--since",
                 "2026-11-05T08:00"]) == 0
    out = capsys.readouterr().out
    assert '"requests": 240' not in out


def test_since_after_last_entry_gives_zero(capsys):
    assert main([SAMPLE, "--since", "2026-11-06T00:00"]) == 0
    assert "Requests:    0" in capsys.readouterr().out


def test_since_rejects_bad_time():
    with pytest.raises(SystemExit):
        main([SAMPLE, "--since", "yesterday"])


def test_since_not_allowed_for_syslog():
    with pytest.raises(SystemExit):
        main(["samples/syslog.log", "--type", "syslog",
              "--since", "2026-11-05T08:00"])
