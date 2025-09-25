# Notion Integration Architecture

Spiceflow Social uses Notion's **official** MCP server (`@notionhq/notion-mcp-server`) to keep Notion as the authoritative store for strategic data while enabling agentic workflows. The server mirrors Notion's OpenAPI surface and works over stdio or authenticated HTTP.

## Notion Data Surfaces
| Database / Page | Purpose | Key Fields | Sync Direction |
| --- | --- | --- | --- |
| Goals & Preferences | Capture long-term objectives, wellbeing guardrails, weighting factors, and qualitative context. | Goal name, category, priority, constraints, notes, last reviewed date. | Notion ➜ Spiceflow (read), Suggestions ➜ Notion (write via Pending Suggestions). |
| Relationship Directory | Track tiers, outreach cadence, last touch, and context notes. | Person, tier, desired cadence, last contact, next touch, notes. | Notion ➜ Spiceflow; cadence tweaks proposed ➜ Notion. |
| Event Calendar Sources | Authoritative list of newsletters, ICS feeds, and websites to scrape. | Source name, URL, topic tags, geo radius, cadence, status. | Notion ➜ Spiceflow; additions/removals proposed ➜ Notion. |
| Pending Suggestions | Queue of AI-drafted updates awaiting approval. | Suggestion summary, category, confidence, linked entities, status. | Spiceflow ➜ Notion (write/read). |
| Evening Recommendations | Weekly 30-day plan with rationale and backups. | Date, recommendation text, linked goals/relationships, intensity, weather risk, status. | Spiceflow ➜ Notion (write); approvals ➜ Spiceflow. |
| Recommendation Feedback | Decisions and qualitative rationale for each recommendation. | Recommendation ref, decision, reason, tags, confidence. | Notion ➜ Spiceflow. |
| Daily Journal | Free-form reflections for NLP. | Date, mood/energy, highlights, challenges, tags, linked goals/relationships. | Notion ➜ Spiceflow (read), optional summary snippets ➜ Notion. |
| Weekly Review Hub | Central review dashboard. | Week range, pending suggestions view, approved events, notes. | Spiceflow ➜ Notion (populate blocks), Human ➜ Notion (approve/comment). |

Templates for each database live in `docs/notion_templates/`. Use `docs/notion_bootstrap.md` for setup instructions.

## Integration Components
- **Official MCP Bridge:** Developers run `@notionhq/notion-mcp-server` locally (or via Docker/hosted) to expose Notion API endpoints as MCP tools. The agent consumes these to provision and maintain databases.
- **Notion Sync Service:** Ingests data via MCP tools (development) or the Notion SDK (production pipeline), storing normalized records and `last_edited_time` checkpoints.
- **Journal Analyzer:** Applies NLP to new journal entries to detect evolving themes, mood trends, and relationship cues. Generates candidate suggestions with provenance.
- **Suggestion Generator:** Combines journal insights, feedback outcomes, and goal progress metrics to populate Pending Suggestions with confidence scores and rationale.
- **Web Scraper Orchestrator:** Fetches activities from Event Calendar Sources, normalizes metadata, and caches events for scoring.
- **Recommendation Engine:** Blends events, availability, goals, relationships, weather, and travel friction into weekly 30-day plans.
- **Approval & Logging Layer:** Writes recommendation packets and suggestion drafts to Notion, tracks approval status changes, and logs the final decisions for audit.

## Cadences & Triggers
| Cadence | Activities |
| --- | --- |
| Daily | Sync journals and feedback, refresh relationship touchpoints, ingest late-breaking events. |
| Weekly (default) | Full event scrape, recompute 30-day plan, draft suggestion batch, publish Weekly Review packet. |
| Monthly | Deep progress review, rotate calendar sources, surface structural goal adjustments. |

Cadences should be configurable (environment variables + Notion properties) and visible in the Weekly Review Hub.

## Human-in-the-Loop Workflow
1. **Sync:** Official MCP server syncs Notion databases into internal models alongside Google availability and weather data.
2. **Analyze:** Journal analyzer and scoring heuristics produce candidate suggestions and events.
3. **Draft:** Suggestions enter Pending Suggestions with `Proposed` status; weekly recommendations post to Evening Recommendations.
4. **Review:** You approve/decline items in Notion (Weekly Review Hub). Approved suggestions trigger updates; rejections are logged with rationale.
5. **Apply:** Agent updates authoritative databases via MCP/SDK and records the action in Recommendation Feedback.
6. **Learn:** Feedback loops adjust scoring weights, suppression timers, and outreach cadences.

## Security & Access
- Use scoped integration capabilities (e.g., read-only during initial testing, upgrade to write when ready).
- Share access only to the root page and databases Spiceflow should manage.
- Store `NOTION_TOKEN` securely (env vars, secret managers); rotate periodically.
- Log every automated write (tooltip, Pending Suggestions, recommendation updates) for transparency.
- Consider Notion's hosted MCP for production to avoid local token storage.

## Implementation Next Steps
1. Build the Notion workspace via `docs/notion_bootstrap.md`.
2. Generate secrets for Notion, Google, weather, travel, and notifications; store them securely.
3. Scaffold the Notion sync service to use MCP tools in development and the SDK/OpenAPI client in deployment.
4. Implement journal NLP pipelines and suggestion drafting logic with provenance tracking.
5. Create the event ingestion orchestrator and caching layer.
6. Publish weekly recommendation packets and hook the approval/feedback loop into Notion databases.

The official server keeps us aligned with Notion's supported tooling while empowering Spiceflow Social to act as an agentic planner inside your workspace.
