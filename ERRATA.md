# Errata and updates

Corrections to *Claude Code: The Practical Guide* (1st edition, 2026) and
notes on changes in Claude Code since the book was tested with version
2.1.331 on November 24, 2026.

## Corrections

None yet. Found a problem? Open an issue in this repository with the page or
section, what the book says, and what you saw.

## Changes in Claude Code since printing

None recorded yet.

## Known notes

- Python 3.12 and 3.13 print `day is out of range for month` where the book
  (tested on Python 3.14) shows `day 31 must be in range 1..30 for month 11 in
  year 2026` (Lab 7.1, step 1). Both are the same `ValueError`.
- The MCP Python SDK 2.x renamed `FastMCP` to `MCPServer`
  (`from mcp.server.mcpserver import MCPServer`). Examples written for 1.x
  fail with 2.x; `ch10/` onward pins `mcp>=2.3,<3`.
