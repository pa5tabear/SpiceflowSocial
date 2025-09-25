# AI Programming Agent Responsibilities (Notion-Integrated)

## Official MCP / SDK Synchronization
- Connect through Notion's official MCP server (`@notionhq/notion-mcp-server`) during development, falling back to the Notion SDK or OpenAPI client with the same token in production services.
- Incrementally sync Goals & Preferences, Relationship Directory, Event Calendar Sources, Pending Suggestions, Evening Recommendations, Recommendation Feedback, Daily Journal, and Weekly Review data using `last_edited_time` checkpoints.
- Prefill Pending Suggestions with proposed updates rather than mutating human-owned entries until approval is granted.

## Journaling & Feedback Analysis
- Parse new journal entries with NLP (sentiment, topic extraction, embeddings) to identify changing goals, relationships, or interests.
- Pair journal insights with recommendation outcomes to prioritize which goals/relationships/sources need revisions.
- Add confidence scores, provenance (journal IDs, feedback references), and rationales to each suggestion created.

## Event Ingestion & Context Enrichment
- Read Event Calendar Sources to orchestrate scraping across ICS feeds, newsletters, and web calendars.
- Enrich events with travel times, intensity classifications, and weather risk metadata.
- Maintain Google Calendar availability for 6–10 PM windows and merge with event timing.
- Pull weather forecasts and location data to filter or annotate activities.

## Recommendation & Review Workflow
- Produce weekly 30-day recommendation packets written to the Evening Recommendations database with preparation notes and backup plans.
- Post summary blocks to the Weekly Review Hub referencing highlights, balance metrics, and pending approvals.
- Monitor approval statuses and log outcomes in Recommendation Feedback for continuous learning.

## Suggestion Lifecycle Automation
- Watch Pending Suggestions for status changes; apply approved updates to the source databases via MCP/SDK calls and log the action with timestamps and actor metadata.
- Cool-down rejected or deferred suggestions to avoid repetition for a configurable window.
- Maintain end-to-end audit trails linking applied changes to originating data (journal entries, recommendation IDs, feedback decisions).

## Operations & Safety
- Schedule daily sync/analyze jobs and weekly full planning runs; expose cadence controls via configuration and Notion properties.
- Handle Notion, Google, weather, and travel API rate limits with retries and circuit breakers; surface issues in observability dashboards.
- Keep tokens/credentials in env vars or secret managers, never in git or Notion properties.
- Emit metrics (suggestions pending, acceptance rates, sync latency) and structured logs for monitoring and alerting.

These responsibilities let the agent automate ingestion, analysis, and orchestration while leaving strategic control firmly in your Notion workspace with human approvals.
