#!/usr/bin/env bash
#
# SOC Assistant — one-shot launcher (Linux / macOS)
# Starts the Flask backend and the Vite frontend, then prints the URLs.
#
# Usage:
#   ./run.sh                 # uses backend/.env if present, else offline/mock mode
#   HF_API_KEY=hf_xxx ./run.sh   # pass a Hugging Face key inline for this run
#
# Stop everything with:  ./stop.sh   (or press Ctrl-C in this terminal)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"
PID_FILE="$ROOT/.run_pids"

# ---- choose python / node binaries ----------------------------------------
PYTHON="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON" ]]; then
  echo "❌ Python 3 not found. Install it:  sudo pacman -S python python-pip"
  exit 1
fi
if ! command -v npm >/dev/null 2>&1; then
  echo "❌ npm not found. Install it:  sudo pacman -S nodejs npm"
  exit 1
fi

echo "==> Using Python: $PYTHON"
echo "==> Using npm   : $(command -v npm)"

# ---------------------------------------------------------------------------
# 1) Backend: venv + deps + .env
# ---------------------------------------------------------------------------
echo
echo "==> Setting up backend..."
cd "$BACKEND"

if [[ ! -d ".venv" ]]; then
  "$PYTHON" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "    created backend/.env from template"
fi

# If HF_API_KEY was provided in the environment, write it into .env
if [[ -n "${HF_API_KEY:-}" ]]; then
  if grep -q '^HF_API_KEY=' .env; then
    sed -i "s|^HF_API_KEY=.*|HF_API_KEY=${HF_API_KEY}|" .env
  else
    echo "HF_API_KEY=${HF_API_KEY}" >> .env
  fi
  if grep -q '^LLM_PROVIDER=' .env; then
    sed -i "s|^LLM_PROVIDER=.*|LLM_PROVIDER=huggingface|" .env
  else
    echo "LLM_PROVIDER=huggingface" >> .env
  fi
  echo "    wrote HF_API_KEY into backend/.env"
fi

# ---------------------------------------------------------------------------
# 2) Frontend: npm install
# ---------------------------------------------------------------------------
echo
echo "==> Setting up frontend (npm install, first run may take a minute)..."
cd "$FRONTEND"
if [[ ! -d "node_modules" ]]; then
  npm install --silent
fi

# ---------------------------------------------------------------------------
# 3) Launch both
# ---------------------------------------------------------------------------
echo
echo "==> Starting servers..."
: > "$PID_FILE"

cd "$BACKEND"
"$BACKEND/.venv/bin/python" app.py > "$ROOT/backend.log" 2>&1 &
echo $! >> "$PID_FILE"

cd "$FRONTEND"
npm run dev > "$ROOT/frontend.log" 2>&1 &
echo $! >> "$PID_FILE"

sleep 4

echo
echo "============================================================"
echo "  🛡️  SOC Assistant is running"
echo "------------------------------------------------------------"
echo "  Frontend : http://localhost:5173"
echo "  Backend  : http://localhost:5000/api/health"
echo "  Logs     : backend.log  /  frontend.log"
echo "  Stop     : ./stop.sh   (or Ctrl-C here)"
echo "============================================================"
echo

# Show backend mode (offline-mock vs huggingface/claude)
sleep 1
curl -s --max-time 5 http://localhost:5000/api/health || true
echo

# Keep running in the foreground; Ctrl-C cleans up.
cleanup() {
  echo; echo "==> Shutting down..."
  while read -r pid; do kill "$pid" 2>/dev/null || true; done < "$PID_FILE"
  rm -f "$PID_FILE"
  exit 0
}
trap cleanup INT TERM
echo "Press Ctrl-C to stop."
wait
