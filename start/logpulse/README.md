# logpulse

A small command-line tool that summarizes an nginx access log or a syslog
file for a morning operations check: request count, status classes, error
rate, slow endpoints, and the programs that logged problems.

It is the running project of *Claude Code: The Practical Guide*
(SysAdmin Knowledge Press). Each chapter's lab changes it.

## Requirements

- Python 3.12 or later
- pytest 8 or later (for the tests)

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
logpulse samples/access.log
logpulse samples/syslog.log --type syslog
logpulse samples/access.log --format json
```

## Test it

```bash
pytest
```

## Access log format

logpulse expects the nginx `combined` format with `$request_time`
appended:

```text
log_format timed '$remote_addr - $remote_user [$time_local] '
                 '"$request" $status $body_bytes_sent '
                 '"$http_referer" "$http_user_agent" $request_time';
```

The files in `samples/` are generated test data. The IP addresses come
from the documentation ranges (RFC 5737).

## License

MIT
