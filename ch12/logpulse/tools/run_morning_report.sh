#!/usr/bin/env bash
# Cron wrapper for tools/morning_report.py. Edit the four paths below.
set -euo pipefail

APP=/opt/logpulse                     # the logpulse checkout
CLAUDE_DIR="$HOME/.local/bin"         # where the claude binary lives
TOKEN_FILE="$HOME/.config/logpulse/claude.env"   # chmod 600
OUT=/var/reports/logpulse

export PATH="$APP/.venv/bin:$CLAUDE_DIR:/usr/bin:/bin"
# The file holds one line: CLAUDE_CODE_OAUTH_TOKEN=... or
# ANTHROPIC_API_KEY=...
set -a
. "$TOKEN_FILE"
set +a

cd "$APP"
python tools/morning_report.py \
  /var/log/nginx/access.log.1 /var/log/syslog.1 "$OUT"
