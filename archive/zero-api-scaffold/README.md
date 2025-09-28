# Spiceflow Social — Zero-API Events → Calendar

**Status:** Scaffold-only. This repo is generated for a future Claude Code desktop run.
**Do not execute any scripts yet.** All entrypoints hard-exit unless `SPICEFLOW_ALLOW_RUN=1`.

## What this is
A macOS-first pipeline that gathers public events (ICS/JSON-LD/HTML/JS), scores them to goals, and emits a single `winners.ics` for Apple Calendar import (which then syncs to Google). It deliberately avoids Google/Notion APIs.

## Why scaffold-only now?
The original plan used Notion/GCal APIs and stalled on OAuth. This repo delivers the same outcome with a file-first contract and ICS import. Today’s task is to **set up** the code and folder structure only.

## When you’re ready to run later
1) Activate venv & install deps.
2) Export your current calendar `.ics` (optional).
3) Set `SPICEFLOW_ALLOW_RUN=1` and run the pipeline.
4) Import `data/out/winners.ics` into Apple Calendar (choose Google calendar).

See comments in `src/run_all.py` for details.
