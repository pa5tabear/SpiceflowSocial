.PHONY: help deps run run-js clean
help:
@echo "Scaffold-only. Set SPICEFLOW_ALLOW_RUN=1 to enable commands later."

deps:
@if [ "$(SPICEFLOW_ALLOW_RUN)" != "1" ]; then echo "Set SPICEFLOW_ALLOW_RUN=1 to install deps later."; exit 1; fi
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && playwright install firefox

run:
@if [ "$(SPICEFLOW_ALLOW_RUN)" != "1" ]; then echo "Scaffold-only"; exit 1; fi
. .venv/bin/activate && python src/run_all.py --horizon-days 45

run-js:
@if [ "$(SPICEFLOW_ALLOW_RUN)" != "1" ]; then echo "Scaffold-only"; exit 1; fi
. .venv/bin/activate && python src/run_all.py --horizon-days 45 --include-js --weekly-pass

clean:
rm -rf data/events_batches/* data/merged/* data/out/*
