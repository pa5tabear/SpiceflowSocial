#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"

cd "$REPO_DIR"

osascript automation/export_availability.applescript

if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

python src/run_all.py --use-llm-research --horizon-days 30 --availability-ics data/availability/calendar.ics

osascript automation/import_to_spiceflow_calendar.applescript
