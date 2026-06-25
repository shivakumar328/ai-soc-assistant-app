#!/usr/bin/env bash
#
# SOC Assistant — stop the servers started by run.sh
#
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT/.run_pids"

if [[ -f "$PID_FILE" ]]; then
  while read -r pid; do
    kill "$pid" 2>/dev/null && echo "stopped PID $pid" || true
  done < "$PID_FILE"
  rm -f "$PID_FILE"
fi

# Fallback: kill anything still bound to the dev ports / app
pkill -f "app.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo "✅ SOC Assistant stopped."
