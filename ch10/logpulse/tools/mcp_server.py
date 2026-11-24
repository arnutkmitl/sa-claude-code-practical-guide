"""A read-only MCP server that answers SQL queries on a logpulse database.

Usage: python tools/mcp_server.py logpulse.db
"""

import sqlite3
import sys

from mcp.server.mcpserver import MCPServer

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "logpulse.db"
MAX_ROWS = 200

server = MCPServer("logpulse-db")


def connect() -> sqlite3.Connection:
    # mode=ro opens the file read-only; query_only blocks writes even
    # if a statement tries.
    db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    db.execute("PRAGMA query_only = ON")
    db.row_factory = sqlite3.Row
    return db


@server.tool()
def schema() -> str:
    """Return the CREATE TABLE statements of the logpulse database."""
    with connect() as db:
        rows = db.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    return "\n\n".join(row["sql"] for row in rows)


@server.tool()
def query(sql: str) -> list[dict]:
    """Run one read-only SELECT on the logpulse database.

    Returns at most 200 rows. The requests table has one row per
    access-log request: ts (local ISO time), ip, method, path, status,
    bytes, and seconds (request time).
    """
    if not sql.lstrip().lower().startswith(("select", "with")):
        raise ValueError("Only SELECT queries are allowed.")
    with connect() as db:
        rows = db.execute(sql).fetchmany(MAX_ROWS)
    return [dict(row) for row in rows]


if __name__ == "__main__":
    server.run()
