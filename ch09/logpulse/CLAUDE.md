# logpulse

Python 3.12+ CLI that summarizes nginx access logs and syslog files.
Code in `src/logpulse/`: `parsers.py` (lines to entries), `report.py`
(entries to numbers and text), `cli.py` (argparse, wiring).

## Commands
- Install for development: `pip install -e ".[dev]"`
- Run all tests: `pytest -q` (must pass before you say a task is done)
- Try the tool: `logpulse samples/access.log`,
  `logpulse samples/syslog.log --type syslog`

## Rules
- Standard library only. Do not add runtime dependencies to
  `pyproject.toml`; ask first if you think one is needed.
- Do not edit files in `samples/`. They are generated test data and
  the numbers in the docs depend on them.
- Every command-line option is documented in `README.md`. When you
  add or change an option, update the README in the same change.
- Errors go to stderr with the prefix `logpulse:`; reports go to stdout.
- Keep lines under 80 characters.

## Git
- Work on a branch, never commit to `main` directly.
- Commit subject: imperative, under 60 characters ("Add --top option").
  Body: why the change was made.

## Known issues
- `parse_access_time()` drops the UTC offset. Don't build features
  that compare times across time zones until it is fixed.

## Compact instructions
When compacting, keep the list of files changed, the test results, and
any rule from this file that was discussed.
