# Sprint Coaching Action Items — 2025-09-28

This backlog turns the sprint coaching memo into concrete follow-up tasks for the
Spiceflow Social pipeline. Track status using the checklist below and link pull
requests as they land.

## High-Priority (blockers for next release)

1. **Availability ingestion MVP** – Create a fixture that represents evening
   free/busy, feed it into portfolio selection, and add CLI flags for swapping
   in Google Calendar exports (`src/plan/choose.py`, `src/run_all.py`).
2. **Preference parser integration** – Load `src/preferences.yaml`, expose the
   data to scoring and selection, and unit-test the translation layer.
3. **Scoring breakdown & category weights** – Extend `src/plan/score.py` to log
   per-component contributions and honor category/goal weights defined in
   preferences.
4. **Portfolio diversity constraints** – Add weekly caps, per-evening guardrails,
   and category quotas before writing `data/out/winners.ics`.
5. **Source reliability sweep** – Harden JSON-LD/HTML scrapers with headers,
   selector fixes, and regression fixtures; fail fast with clear telemetry
   (`src/scrape/*`, `src/emit/reports.py`).

## Secondary (quality & observability)

6. **Run report enhancements** – Port Nesting's digest/report structure so each
   run outputs timings, cache hits, and per-source results.
7. **Dedupe ledger relocation** – Move the registry under `data/` and attach
   `first_seen`/`last_seen` metadata for provenance (`src/util/dedupe.py`).
8. **Change budget + anti-churn** – Enforce freeze windows and swap thresholds
   from `preferences.yaml` when proposing updates.
9. **Tests & smoke scripts** – Stand up `tests/` with unit coverage for scoring,
   dedupe, and selection; add a smoke CLI that verifies parsers without hitting
   the network.

## Longer-Term Improvements

10. **Availability integration with Google/O365** – Replace the fixture with
    real API calls once credentials are ready.
11. **Weather/travel enrichment** – Add placeholder adapters so future sprints
    can compute friction scores tied to travel bins.
12. **Feedback loop & ledger** – Store approved/rejected recommendations, then
    feed the outcomes back into the scoring config.

## Immediate Next Steps

- Groom items 1–5 into executable cards with acceptance criteria.
- Identify owners and sprint load for availability + preferences work first.
- Schedule a code review check-in once the fixture-backed availability pipeline
  is merged.
