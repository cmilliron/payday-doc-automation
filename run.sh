#!/usr/bin/env bash
set -e

# Resolve the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Determine the Python executable to use
if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"
elif command -v uv >/dev/null 2>&1; then
    PYTHON_EXEC="uv run python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_EXEC="python3"
else
    PYTHON_EXEC="python"
fi

# Run main.py with any passed arguments
$PYTHON_EXEC "$SCRIPT_DIR/main.py" "$@"
