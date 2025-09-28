#!/bin/bash

# daily_research.sh
# Owner: Gemini
# Purpose: Automates the daily run of the Spiceflow Social pipeline for event curation.

# --- Configuration ---
set -e  # Exit immediately if a command exits with a non-zero status.

# Assuming this script is run from the project root.
# If not, uncomment and set the correct project directory.
# PROJECT_DIR="/path/to/your/SpiceflowSocial"
PROJECT_DIR=$(pwd)

DATA_DIR="$PROJECT_DIR/data"
ARCHIVE_DIR="$DATA_DIR/archive"
OUTPUT_DIR="$DATA_DIR/out"

# --- Timestamp and Archive Setup ---
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
DAILY_ARCHIVE_DIR="$ARCHIVE_DIR/$TIMESTAMP"

echo "[INFO] Creating archive directory: $DAILY_ARCHIVE_DIR"
mkdir -p "$DAILY_ARCHIVE_DIR"

# --- Main Pipeline Execution ---
echo "[INFO] Starting daily Spiceflow Social pipeline run..."

# Activate virtual environment if it exists
if [ -d "$PROJECT_DIR/.venv" ]; then
    echo "[INFO] Activating Python virtual environment..."
    source "$PROJECT_DIR/.venv/bin/activate"
fi

# Run the pipeline with rolling update mode.
# This preserves existing user selections and adds suggestions for the new day.
python "$PROJECT_DIR/src/run_all.py" --rolling-update --horizon-days 7

PIPELINE_EXIT_CODE=$?

if [ $PIPELINE_EXIT_CODE -ne 0 ]; then
    echo "[ERROR] Pipeline execution failed with exit code $PIPELINE_EXIT_CODE."
    exit 1
fi

echo "[INFO] Pipeline execution completed successfully."

# --- Archive Outputs ---
echo "[INFO] Archiving key outputs..."

cp "$OUTPUT_DIR/winners.ics" "$DAILY_ARCHIVE_DIR/winners.ics"
cp "$OUTPUT_DIR/weekly_review.md" "$DAILY_ARCHIVE_DIR/weekly_review.md"

# run_summary.json is expected to be created by Cursor's part of the plan
if [ -f "$OUTPUT_DIR/run_summary.json" ]; then
    cp "$OUTPUT_DIR/run_summary.json" "$DAILY_ARCHIVE_DIR/run_summary.json"
else
    echo "[WARN] run_summary.json not found. Skipping summary."
fi

# --- Print Summary ---
echo "[INFO] Daily run summary:"
echo "-------------------------"

if [ -f "$DAILY_ARCHIVE_DIR/run_summary.json" ]; then
    # Use jq for pretty-printing if available, otherwise just cat
    if command -v jq &> /dev/null
    then
        jq . "$DAILY_-DIR/run_summary.json"
    else
        cat "$DAILY_ARCHIVE_DIR/run_summary.json"
    fi
else
    echo "No summary data available."
fi

echo "-------------------------"
echo "[SUCCESS] Daily run complete. Artifacts archived in $DAILY_ARCHIVE_DIR"
