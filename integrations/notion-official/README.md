# Official Notion MCP Server

Spiceflow Social uses Notion's **official** MCP server (`@notionhq/notion-mcp-server`) to read and write workspace data through Model Context Protocol clients.

## Installation Options

### 1. `npx`
```bash
export NOTION_TOKEN="ntn_..."   # Internal integration token from notion.so/my-integrations
npx @notionhq/notion-mcp-server
```
This starts the server over stdio, which works with Cursor, Claude Desktop, Cline, Zed, and other MCP-aware clients.

### 2. Docker
```bash
docker run --rm -i -e NOTION_TOKEN=ntn_... mcp/notion
```
For custom builds:
```bash
docker compose build
NOTION_TOKEN=ntn_... docker run --rm -i notion-mcp-server
```

### 3. Hosted Remote MCP (beta)
Notion offers a hosted version that connects via OAuth with zero local setup. See the [docs](https://developers.notion.com/docs/mcp) for access and configuration.

## Client Configuration Samples

### Cursor / Claude Desktop (`mcp.json`)
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_..."
      }
    }
  }
}
```

### Zed (`settings.json`)
```json
{
  "context_servers": {
    "notion": {
      "command": {
        "path": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env": {
          "NOTION_TOKEN": "ntn_..."
        }
      }
    }
  }
}
```

For HTTP transport add `--transport http --port 3000` and supply `AUTH_TOKEN` or `--auth-token`.

## Scoping the Integration
1. Create an internal integration in Notion named `Spiceflow Social`.
2. Limit capabilities as desired (read-only, no user info, etc.).
3. Share only the root page and databases the assistant should access.
4. Rotate the token periodically and store it via environment variables or a secret manager.

With the server running, follow `docs/notion_bootstrap.md` to create databases using MCP calls and keep Notion as the source of truth.
