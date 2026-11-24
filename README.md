# Claude Code: The Practical Guide — companion code

Code for the book *Claude Code: The Practical Guide: Agentic Coding and
Automation for Developers, Sysadmins, and DevOps Engineers* by Arnut
Ruttanatirakul (SysAdmin Knowledge Press, 2026). AI Automation Series, Vol. 2.

The book builds one project, **logpulse**, a small Python tool that
summarizes nginx access logs and syslog files. Each directory holds the
project as it is at that point in the book.

| Directory | State of logpulse | Book |
|---|---|---|
| `start/` | Starting point (labs 1.1 and 2.1 begin here) | Chapters 1-2 |
| `ch03/` | `--since` option | Lab 3.1 |
| `ch04/` | `CLAUDE.md` and `.claude/rules/tests.md` | Lab 4.1 |
| `ch05/` | `.claude/settings.json` permission rules | Lab 5.1 |
| `ch06/` | Syslog detects "timed out" and OOM kills | Lab 6.1 |
| `ch07/` | Impossible-date fix and refactor; `bad-date.log` | Lab 7.1 |
| `ch08/` | `release-notes` skill and `CHANGELOG.md` | Lab 8.1 |
| `ch09/` | ruff formatting and two hooks | Lab 9.1 |
| `ch10/` | SQLite export and read-only MCP server | Lab 10.1 |
| `ch11/` | `security-reviewer` subagent | Lab 11.1 |
| `ch12/` | Morning report, cron wrapper, PR review workflow | Lab 12.1 |

The solutions are references. Your code will differ in detail; compare the
behavior (the tests and the outputs the lab names), not the text.

## Requirements

- Python 3.12 or later, Git
- Claude Code (tested with 2.1.331)
- For `ch10/` onward: `pip install -r tools/requirements-mcp.txt`

## Run a stage

```bash
cd ch07/logpulse
python -m venv .venv
source .venv/bin/activate        # Windows (Git Bash): source .venv/Scripts/activate
pip install -e ".[dev]"
pytest -q
```

## Corrections and updates

Claude Code changes quickly. See [ERRATA.md](ERRATA.md) for corrections and
for changes in Claude Code since the book was printed.

## License

The code is released under the MIT License (see [LICENSE](LICENSE)). The
sample logs in `samples/` are generated data; their IP addresses are from
the documentation ranges in RFC 5737.

Publisher: SysAdmin Knowledge Press, https://www.sysadmin.in.th
