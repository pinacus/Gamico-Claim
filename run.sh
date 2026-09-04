
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DISPLAY_NUMBER="${DISPLAY_NUMBER:-auto}"

if [[ ! -x "$PROJECT_DIR/.venv/bin/python" ]]; then
	echo "Python virtual environment not found at $PROJECT_DIR/.venv" >&2
	exit 1
fi

if ! command -v xvfb-run >/dev/null 2>&1; then
	echo "xvfb-run is required. Install the Xvfb package with your system package manager." >&2
	exit 1
fi

cd "$PROJECT_DIR"

XVFB_ARGS=(--server-args="-screen 0 1280x1024x24")
if [[ "$DISPLAY_NUMBER" == "auto" ]]; then
	XVFB_ARGS+=(--auto-servernum)
else
	XVFB_ARGS+=(--server-num="$DISPLAY_NUMBER")
fi

exec xvfb-run "${XVFB_ARGS[@]}" "$PROJECT_DIR/.venv/bin/python" -m src.epic_games.claim_game
