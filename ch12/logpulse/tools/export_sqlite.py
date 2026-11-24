"""Load an nginx access log into a SQLite database for ad hoc queries.

Usage: python tools/export_sqlite.py samples/access.log logpulse.db
"""

import sqlite3
import sys

from logpulse.parsers import read_access_log

SCHEMA = """
CREATE TABLE IF NOT EXISTS requests (
    ts      TEXT NOT NULL,   -- local time, ISO 8601
    ip      TEXT NOT NULL,
    method  TEXT NOT NULL,
    path    TEXT NOT NULL,
    status  INTEGER NOT NULL,
    bytes   INTEGER NOT NULL,
    seconds REAL NOT NULL
)
"""


def main(log_path: str, db_path: str) -> int:
    entries, skipped = read_access_log(log_path)
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TABLE IF EXISTS requests")
        db.execute(SCHEMA)
        db.executemany(
            "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    e.time.isoformat(),
                    e.ip,
                    e.method,
                    e.path,
                    e.status,
                    e.size,
                    e.request_time,
                )
                for e in entries
            ],
        )
    msg = f"Loaded {len(entries)} requests into {db_path}"
    print(f"{msg} ({skipped} skipped)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
