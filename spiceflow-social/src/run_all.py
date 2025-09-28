import os, sys, json, argparse, pathlib
from rich import print

# HARD SAFETY: scaffold-only until explicitly enabled
if os.environ.get("SPICEFLOW_ALLOW_RUN","0") != "1":
    print("[SCaffold Mode] SPICEFLOW_ALLOW_RUN != 1 → exiting without execution.")
    sys.exit(0)

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BATCH_DIR = DATA / "events_batches"
MERGED_DIR = DATA / "merged"
OUT_DIR = DATA / "out"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon-days", type=int, default=45)
    ap.add_argument("--include-js", action="store_true")
    ap.add_argument("--weekly-pass", action="store_true")
    args = ap.parse_args()

    # Future flow (documented, not executed during scaffold gen):
    # 1) load sources.yaml
    # 2) parallel scrape Tier A (ics/jsonld/html); optionally Tier B (js)
    # 3) write per-source jsonl/ics in batch folder
    # 4) merge+dedupe -> merged/all_events.jsonl
    # 5) score & choose -> out/portfolio.json
    # 6) emit winners.ics (+ winners-REMOVE.ics) in out/

    print(f"[DRY] Would run full pipeline with horizon={args.horizon_days}, include_js={args.include_js}, weekly={args.weekly_pass}")
    print(f"[DRY] Output dirs:\n  {BATCH_DIR}\n  {MERGED_DIR}\n  {OUT_DIR}")

if __name__ == "__main__":
    main()
