# AI Programming Agent Responsibilities (Notion-Integrated)

## Notion Synchronization
- Connect to designated Notion databases (Goals & Preferences, Relationship Directory, Event Calendar Sources, Feedback Log, Daily Journals, Weekly Review Hub) via integration token with minimal scopes.
- Normalize Notion records into internal domain models, tracking `last_edited_time` for incremental syncs.
- Write suggestion objects and weekly recommendation summaries back into Notion (e.g., "Pending Suggestions" and "Weekly Review Hub" views) without altering approved human-authored entries directly.

## Journaling & Feedback Analysis
- Process new daily journal entries with NLP pipelines (sentiment, key phrase extraction, topic clustering) to detect shifts in goals, relationship sentiments, or emerging interests.
- Cross-reference feedback log outcomes to identify patterns in accepted vs. rejected recommendations.
- Generate suggestion drafts for goal adjustments, relationship cadence tweaks, or new event sources, tagging each with confidence and rationale.

## Event Ingestion & Context Enrichment
- Read the Event Calendar Sources database to assemble scraping targets (ICS feeds, newsletters, HTML pages) and ingest fresh events on the configured schedule.
- Enrich events with travel-time estimates, intensity classifications, and weather sensitivity metadata using external APIs.
- Maintain availability timelines by syncing Google Calendar free/busy data for 6–10 PM windows.
- Pull weather forecasts and location data to apply contextual filters before scoring.

## Recommendation & Review Workflow
- Run weekly (configurable) recommendation cycles that produce a 30-day lookahead of evening suggestions with ranked options and fallback activities.
- Post recommendation summaries to the Weekly Review Hub, including justification, preparation notes, and backup choices.
- Monitor approval statuses and feed results into the feedback log for continuous learning.

## Suggestion Lifecycle Automation
- When humans approve suggestions in Notion, queue update jobs that apply the accepted changes to the relevant databases (e.g., update goal weighting fields, add a new calendar source entry).
- Respect "Rejected" or "Deferred" statuses by suppressing repeated proposals for a configurable cool-down period.
- Maintain audit logs linking suggestions to their originating journal entries or feedback signals.

## Operations & Safety
- Schedule daily lightweight syncs (journals, feedback) and weekly deep runs (event scraping, recommendation refresh, suggestion drafting).
- Handle API rate limits and failures gracefully with retries and notifications.
- Protect secrets (Notion token, Google credentials, weather/travel keys) using environment variables or secret managers.
- Expose observability hooks (metrics, logs, alerts) to signal integration health and data drift.

These responsibilities ensure the agent automates intelligence and orchestration while leaving strategic control and approvals firmly in human hands within Notion.
