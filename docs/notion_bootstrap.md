# Notion Bootstrap Guide (Official MCP)

This guide converts a blank Notion workspace into the Spiceflow Social command center using Notion's official MCP server (`@notionhq/notion-mcp-server`).

## 1. Create the Integration & Root Page
1. Visit [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) and create a new **internal integration** named `Spiceflow Social`.
2. Copy the generated **Internal Integration Token** (`ntn_…`).
3. In Notion, create a root page (e.g., `Spiceflow Social Hub`). Copy its page ID from the URL (strip hyphens).
4. Share the page with your integration (⋯ → **Connections** → `Spiceflow Social`).

You now have:
- `NOTION_TOKEN`: the integration token.
- `PARENT_PAGE_ID`: the ID of the root hub page.

> 🔒 Scope the integration to only the pages/databases Spiceflow needs. You can make it read-only initially and unlock actions later.

## 2. Run the Official MCP Server
Choose your preferred option. See `integrations/notion-official/README.md` for details.

### StdIO (Cursor, Claude Desktop, etc.)
```bash
export NOTION_TOKEN="ntn_..."
npx @notionhq/notion-mcp-server
```

### Docker
```bash
docker run --rm -i -e NOTION_TOKEN=ntn_... mcp/notion
```

### Hosted (Beta)
If you're part of the hosted MCP beta, follow the OAuth flow at [developers.notion.com/docs/mcp](https://developers.notion.com/docs/mcp) and skip local setup.

Connect your MCP-capable client to the running server. Listing tools should reveal dozens of endpoints (e.g., `notionApi-v1-databases-query`).

## 3. Create Core Databases
Use the JSON payload templates in `docs/notion_templates/` with the `notionApi-v1-databases-create` tool.

1. Open a template such as `docs/notion_templates/goals_preferences.json`.
2. Replace all placeholders:
   - `PARENT_PAGE_ID` → your root page ID.
   - Relation IDs (e.g., `GOALS_DATABASE_ID`) → fill in after the referenced database is created. You can leave them blank at creation time and add relations later via UI or PATCH.
3. Invoke the tool:
```json
{
  "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
  "title": [...],
  "properties": {...}
}
```
4. Note the database ID returned in the response.

Recommended order (so you can link relations as you go):
1. Goals & Preferences
2. Relationship Directory
3. Event Calendar Sources
4. Pending Suggestions
5. Evening Recommendations
6. Recommendation Feedback
7. Daily Journal
8. Weekly Review Tracker

> ℹ️ If you prefer, you can add relations after creation through the Notion UI. Update the templates or use `notionApi-v1-databases-update` once IDs are known.

## 4. Build the Weekly Review Hub Page
Create a dashboard page under the root hub using `notionApi-v1-pages-create` and the payload below:
```json
{
  "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
  "properties": {
    "title": {
      "title": [{"text": {"content": "Weekly Review Hub"}}]
    }
  },
  "children": [
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "Pending Suggestions"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Drop in a linked view of the Pending Suggestions database filtered to status = Proposed."}}]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "Approved Calendar Plan"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Show the 30-day recommendation packet and decision log here."}}]
      }
    }
  ]
}
```
Then, inside Notion, add linked database views for Pending Suggestions, Evening Recommendations, Recommendation Feedback, and any recap you want.

## 5. Populate Initial Data
- Enter your current goals, preferences, and wellbeing guardrails.
- Seed the relationship directory with key contacts and cadence targets.
- List your event calendar sources with tags and refresh cadence.
- Start journaling daily entries, tagging highlights and challenges.

## 6. Configure Secrets for the Codebase
Create `/.env` (git-ignored) with:
```env
NOTION_TOKEN=ntn_...
NOTION_ROOT_PAGE_ID=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
WEATHER_API_KEY=...
TRAVEL_API_KEY=...
```
These feed the upcoming sync services. For production, store them in a secret manager.

## 7. Automate Cadences (Later)
Once the workspace structure is stable:
- Schedule daily syncs for journals, feedback, and upcoming recommendations.
- Schedule weekly runs that scrape events, refresh the 30-day plan, and draft suggestions.
- Make monthly or quarterly reviews part of the Weekly Review Hub template.

With the official MCP server in place, Spiceflow Social can programmatically build and maintain the workspace while you stay in the approval loop.
