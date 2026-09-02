#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8080}"

printf '\nPersonal Assistant\n'
printf '%s\n' '================='
printf 'Project: %s\n' "$PROJECT_DIR"
printf 'Address: http://%s:%s\n\n' "$HOST" "$PORT"

if ! command -v uv >/dev/null 2>&1; then
  printf '%s\n' 'Error: uv is required but was not found.' >&2
  printf '%s\n' 'Install it from https://docs.astral.sh/uv/getting-started/installation/' >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  printf '%s\n' 'Warning: .env was not found. Model requests may fail authentication.' >&2
  printf '%s\n\n' 'Create .env from the examples in README.md.' >&2
fi

printf '%s\n' 'Step 1/4: Syncing dependencies...'
uv sync

printf '%s\n' 'Step 2/4: Initializing the database...'
uv run python init_db.py

printf '%s\n' 'Step 3/4: Checking Python files...'
uv run python -m py_compile \
  main.py web_app.py init_db.py \
  personal_assistant/*.py \
  claude_agent/agent.py gemini_agent/agent.py openai_agent/agent.py \
  tools/*.py

printf '%s\n' 'Step 4/4: Starting the web UI...'
printf 'Open http://%s:%s in your browser. Press Ctrl+C to stop.\n\n' "$HOST" "$PORT"
HOST="$HOST" PORT="$PORT" uv run python main.py
