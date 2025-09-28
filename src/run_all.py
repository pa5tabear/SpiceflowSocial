"""Spiceflow Social end-to-end runner."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import yaml

from emit.ics_writer import write_ics
from emit.reports import write_run_report
from plan.choose import choose_portfolio, write_portfolio
from plan.score import attach_scores
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

SOURCE_LINE_RE = re.compile(r"^\s*-\s*\[(?P<name>.+?)\]\((?P<url>[^)]+)\)\s*(?:\|\s*(?P<meta>.*))?$")


def _assign_nested(target: dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    current = target
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value


def parse_markdown_sources(text: str) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    in_code_block = False
    for index, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith("-[") and not stripped.startswith("- ["):
            continue
        match = SOURCE_LINE_RE.match(stripped)
        if not match:
            raise ValueError(f"Invalid source definition on line {index}: {raw_line.strip()}")
        entry: dict[str, Any] = {
            "name": match.group("name").strip(),
            "url": match.group("url").strip(),
        }
        meta_block = match.group("meta") or ""
        meta: dict[str, Any] = {}
        if meta_block:
            for chunk in meta_block.split("|"):
                chunk = chunk.strip()
                if not chunk:
                    continue
                if "=" not in chunk:
                    raise ValueError(f"Missing '=' in metadata chunk '{chunk}' on line {index}")
                key, value = chunk.split("=", 1)
                value = value.strip()
                parsed_value = yaml.safe_load(value) if value else None
                _assign_nested(meta, key.strip(), parsed_value)
        entry.update(meta)
        if "type" not in entry and "kind" in entry:
            entry["type"] = entry.pop("kind")
        if "type" not in entry and "parser" in entry:
            entry["type"] = entry.pop("parser")
        if "slug" not in entry:
            raise ValueError(f"Missing 'slug' for source on line {index}")
        if "type" not in entry:
            raise ValueError(f"Missing 'type' for source '{entry['slug']}' on line {index}")
        sources.append(entry)
    return sources


def load_sources(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Source registry not found at {path}")
    text = path.read_text()
    if path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text) or []
        if not isinstance(data, list):
            raise ValueError("YAML sources file must be a list of entries")
        return data
    return parse_markdown_sources(text)


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
    parser.add_argument("--sources", type=Path, default=Path("src/sources.yaml"))
    parser.add_argument("--scoring-config", type=Path, default=Path("src/scoring_config.json"))
    parser.add_argument("--registry", type=Path, default=Path("src/registry.json"))
    args = parser.parse_args()

    sources = load_sources(args.sources)
    scoring_config = load_scoring_config(args.scoring_config)

    run_date = datetime.now(DEFAULT_TIMEZONE).date().isoformat()
    batch_dir = Path("data/events_batches") / f"batch_{run_date}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    all_events: list[dict[str, Any]] = []
    skipped_sources: list[str] = []

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
        else:
            skipped_sources.append(slug)

    unique_events, duplicates = dedupe_events(all_events, args.registry)
    attach_scores(unique_events, scoring_config)

    merged_jsonl = Path("data/merged/all_events.jsonl")
    merged_ics = Path("data/merged/all_events.ics")
    write_jsonl(merged_jsonl, unique_events)
    write_ics(unique_events, merged_ics, calendar_name="Spiceflow Social — merged")

    portfolio = choose_portfolio(unique_events, scoring_config)
    portfolio_path = Path("data/out/portfolio.json")
    write_portfolio(portfolio, portfolio_path)

    winners_ics = Path("data/out/winners.ics")
    write_ics(portfolio["selected"], winners_ics, calendar_name="Spiceflow Social — winners")
    winners_remove = Path("data/out/winners-REMOVE.ics")
    write_ics(portfolio["selected"], winners_remove, calendar_name="Spiceflow Social — rollback", cancelled=True)

    run_report_path = batch_dir / "run_report.md"
    write_run_report(run_report_path, events=unique_events, duplicates=duplicates, skipped_sources=skipped_sources)

    print(f"Run complete: {len(unique_events)} events, {len(portfolio['selected'])} selected")


if __name__ == "__main__":
    main()
