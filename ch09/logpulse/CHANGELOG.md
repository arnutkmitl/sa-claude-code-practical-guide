# Changelog

## 0.2.0 - 2026-11-24

### Added

- `--since TIME` option to report only access-log entries at or
  after an ISO time (for example `2026-11-24T06:00`). Works only
  with `--type access`.

### Changed

- Syslog lines mentioning "timed out", "out of memory" or
  "killed process" now count as problems, so nginx upstream
  timeouts and OOM kills show up in the report.

### Fixed

- Access-log lines with impossible dates (such as 31 Nov) are now
  counted as skipped instead of crashing logpulse.

## 0.1.0 - 2026-11-05

### Added

- First release: summarize nginx access logs and syslog files
  as text or JSON.
