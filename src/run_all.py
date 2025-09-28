"""Spiceflow Social end-to-end runner."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import yaml

from emit.ics_writer import write_ics
from emit.reports import write_run_report
from emit.research_report import write_research_summary
from emit.daily_markdown import write_daily_markdowns, write_changes_summary
from emit.weekly_review import write_weekly_review
from emit.source_performance_report import write_source_performance_report
from plan.choose import choose_portfolio, write_portfolio
from plan.score import attach_scores
from preferences import load_preferences, target_calendar_name
from research import gather_llm_research
from availability import load_calendar_events, summarise_evenings, write_availability_markdown
from emit.shortlist import write_shortlist_report
from util.dedupe import dedupe_events
from util.timez import DEFAULT_TIMEZONE

from scrape import html_pull, ics_pull, jsonld_pull, js_pull

SCRAPER_ORDER = ["ics", "jsonld", "html", "js"]
SCRAPERS = {
    "ics": ics_pull.pull,
    "jsonld": jsonld_pull.pull,
    "html": html_pull.pull,
    "js": js_pull.pull,
}


def load_sources(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Source registry not found at {path}")
    if path.suffix not in {".yaml", ".yml"}:
        raise ValueError("`sources.yaml` must be a YAML list of source entries")
    data = yaml.safe_load(path.read_text()) or []
    if not isinstance(data, list):
        raise ValueError("YAML sources file must be a list of entries")
    return data


def load_scoring_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"scoring_config.json not found at {path}")
    return json.loads(path.read_text())


def write_jsonl(path: Path, events: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def process_source(source: dict[str, Any], *, horizon_days: int, include_js: bool) -> tuple[list[dict[str, Any]], str]:
    slug = source.get("slug")
    preferred_type = source.get("type")
    tried: list[str] = []
    for type_name in ([preferred_type] if preferred_type else SCRAPER_ORDER):
        if type_name == "js" and not include_js:
            continue
        scraper = SCRAPERS.get(type_name)
        if not scraper:
            continue
        tried.append(type_name)
        try:
            events = scraper(source, horizon_days=horizon_days)
        except NotImplementedError:
            continue
        except Exception as exc:
            print(f"[warn] {slug}: {type_name} scraper failed — {exc}")
            continue
        if events:
            return events, type_name
    return [], tried[-1] if tried else (preferred_type or "unknown")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Spiceflow Social pipeline")
    parser.add_argument("--horizon-days", type=int, default=45)
    parser.add_argument("--include-js", action="store_true", help="Allow Playwright-backed JS scrapers")
    parser.add_argument("--weekly-pass", action="store_true", help="Tag this run as the weekly JS sweep")
    parser.add_argument("--use-llm-research", action="store_true", help="Use LLM research instead of direct scraping")
    parser.add_argument("--llm-overwrite", action="store_true", help="Overwrite LLM snapshots instead of timestamped files")
    parser.add_argument("--rolling-update", action="store_true", help="Daily rolling update mode (preserve approvals, append new day)")
    parser.add_argument("--full-refresh", action="store_true", help="Full 7-day refresh mode (regenerate all selections)")
    parser.add_argument("--sources", type=Path, default=Path("src/sources.yaml"))
    parser.add_argument("--scoring-config", type=Path, default=Path("src/scoring_config.json"))
    parser.add_argument("--preferences", type=Path, default=Path("src/preferences.yaml"))
    parser.add_argument("--registry", type=Path, default=Path("src/registry.json"))
    parser.add_argument("--availability-ics", type=Path, default=Path("data/availability/calendar.ics"))
    args = parser.parse_args()

    sources = load_sources(args.sources)
    scoring_config = load_scoring_config(args.scoring_config)
    preferences = load_preferences(args.preferences)

    availability_summary = {}
    if args.availability_ics and args.availability_ics.exists():
        availability_events = load_calendar_events(args.availability_ics)
        availability_summary = summarise_evenings(availability_events, preferences=preferences, horizon_days=args.horizon_days)
        if availability_summary:
            write_availability_markdown(Path('data/out/availability.md'), availability_summary)

    run_date = datetime.now(DEFAULT_TIMEZONE).date().isoformat()
    batch_dir = Path("data/events_batches") / f"batch_{run_date}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    all_events: list[dict[str, Any]] = []
    skipped_sources: list[str] = []
    research_summaries: list[dict[str, Any]] = []
    research_entries: list[dict[str, Any]] = []
    counts_by_slug: dict[str, int] = {}

    source_lookup = {source.get("slug"): source for source in sources if source.get("slug")}

    if args.use_llm_research:
        research_dir = Path("data/research")
        llm_events, results = gather_llm_research(
            sources,
            horizon_days=args.horizon_days,
            output_dir=research_dir,
            overwrite=args.llm_overwrite,
        )
        events_by_slug: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in llm_events:
            all_events.append(item)
            events_by_slug[item.get("source", "unknown")].append(item)
        for slug, items in events_by_slug.items():
            counts_by_slug[slug] = len(items)
        for result in results:
            slug = result.slug or "source"
            research_entries.append({"slug": slug, "summary": result.summary, "notes": result.notes})
            research_summaries.append({"slug": slug, "summary": result.summary})
            events = events_by_slug.get(slug, [])
            source_jsonl = batch_dir / f"{slug}.jsonl"
            source_ics = batch_dir / f"{slug}.ics"
            write_jsonl(source_jsonl, events)
            if events:
                calendar_name = source_lookup.get(slug, {}).get("name", slug)
                write_ics(events, source_ics, calendar_name=calendar_name)
            else:
                skipped_sources.append(slug)
    else:
        for source in sources:
            if source.get("type") == "js" and not args.include_js:
                skipped_sources.append(source.get("slug", "unknown"))
                continue
            events, _ = process_source(source, horizon_days=args.horizon_days, include_js=args.include_js)
            slug = source.get("slug", "source")
            source_jsonl = batch_dir / f"{slug}.jsonl"
            source_ics = batch_dir / f"{slug}.ics"
            write_jsonl(source_jsonl, events)
            if events:
                write_ics(events, source_ics, calendar_name=source.get("name", slug))
                all_events.extend(events)
                counts_by_slug[slug] = len(events)
            else:
                skipped_sources.append(slug)

    unique_events, duplicates = dedupe_events(all_events, args.registry)
    attach_scores(unique_events, scoring_config, preferences)

    if research_entries:
        write_research_summary(Path("data/out/research_summary.md"), research_entries)

    merged_jsonl = Path("data/merged/all_events.jsonl")
    merged_ics = Path("data/merged/all_events.ics")
    write_jsonl(merged_jsonl, unique_events)
    write_ics(unique_events, merged_ics, calendar_name="Spiceflow Social — merged")

    portfolio = choose_portfolio(unique_events, scoring_config, preferences)
    portfolio_path = Path("data/out/portfolio.json")
    write_portfolio(portfolio, portfolio_path)
    write_shortlist_report(Path("data/out/shortlist.md"), portfolio["selected"])

    target_calendar = target_calendar_name(preferences)
    winners_ics = Path("data/out/winners.ics")
    write_ics(portfolio["selected"], winners_ics, calendar_name=target_calendar)
    winners_remove = Path("data/out/winners-REMOVE.ics")
    write_ics(portfolio["selected"], winners_remove, calendar_name=f"{target_calendar} (Rollback)", cancelled=True)

    daily_info = write_daily_markdowns(
        portfolio["selected"],
        availability_summary,
        horizon_days=min(args.horizon_days, 7),
        output_dir=Path("data/out/daily"),
    )
    write_changes_summary(Path("data/out/suggested_changes.md"), daily_info)

    # Weekly review (preserve approvals if rolling update)
    previous_selected = None
    archive_dir = Path("data/out/portfolios")
    archive_dir.mkdir(parents=True, exist_ok=True)
    latest_prev = None
    prev_files = sorted(archive_dir.glob("portfolio-*.json"))
    if prev_files:
        latest_prev = prev_files[-1]
    if latest_prev and args.rolling_update:
        try:
            previous_selected = json.loads(latest_prev.read_text()).get("selected", [])
        except Exception:
            previous_selected = None
    write_weekly_review(
        portfolio["selected"],
        portfolio,
        availability_summary,
        Path("data/out/weekly_review.md"),
        previous_selected=previous_selected,
    )
    # Archive current portfolio
    archive_path = archive_dir / f"portfolio-{run_date}.json"
    try:
        archive_path.write_text(json.dumps(portfolio, ensure_ascii=False, indent=2))
    except Exception:
        pass

    run_report_path = batch_dir / "run_report.md"
    write_run_report(
        run_report_path,
        events=unique_events,
        duplicates=duplicates,
        skipped_sources=skipped_sources,
        portfolio_summary=portfolio.get("summary"),
        research_summaries=research_summaries,
        availability_summary=availability_summary if availability_summary else None,
    )

    # Simple source performance report
    write_source_performance_report(counts_by_slug, skipped_sources, Path("data/out/source_performance_report.md"))

    # Run summary JSON for automation/scripts
    run_summary = {
        "date": run_date,
        "num_sources": len(sources),
        "num_unique_events": len(unique_events),
        "num_selected": len(portfolio["selected"]),
        "num_duplicates": len(duplicates),
        "skipped_sources": skipped_sources,
    }
    try:
        Path("data/out/run_summary.json").write_text(json.dumps(run_summary, ensure_ascii=False, indent=2))
    except Exception:
        pass

    print(f"Run complete: {len(unique_events)} events, {len(portfolio['selected'])} selected")


if __name__ == "__main__":
    main()
