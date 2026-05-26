# Fireslide Codex Plugin

Fireslide is a thin Codex plugin that connects Codex to the hosted Fireslide MCP server.

It lets Codex create editable slide decks, choose Fireslide styles, use media/news tools, and return a Fireslide editor URL.

The plugin does not include the Fireslide backend or renderer. It only points supported agents at the hosted MCP endpoint.

## What This Repo Contains

- Codex plugin metadata
- A remote MCP server config pointing to `https://mcp.fireslide.ai/`
- A Codex skill that teaches the deck-creation workflow
- Public setup documentation

## What This Repo Does Not Contain

- Fireslide backend source code
- Renderer implementation
- Style catalog internals
- Auth service code
- API keys or secrets
- Paid media/news provider credentials

All proprietary product logic stays behind the hosted Fireslide MCP service.

## MCP Server

The plugin connects to:

```text
https://mcp.fireslide.ai/
```

On first use, Codex will authenticate through Fireslide OAuth.

## Main Tools

The hosted MCP server exposes tools including:

- `list_styles`
- `get_style`
- `render_presentation`
- `search_images`
- `generate_image`
- `make_svg`
- `make_meme`
- `search_news`

## Local Install

Install this plugin through Codex's plugin UI from this repository, or clone it locally and point Codex at the plugin folder.

The plugin root is the folder that contains:

```text
.codex-plugin/plugin.json
.mcp.json
skills/
```

## Claude Code

Claude Code does not need the Codex plugin wrapper. It can connect to the same hosted MCP server directly:

```bash
claude mcp add --transport http fireslide https://mcp.fireslide.ai/
```

On first use, Claude Code should open the Fireslide OAuth flow. After auth, the same hosted MCP tools are available.

If your client prefers JSON config, use:

```json
{
  "mcpServers": {
    "fireslide": {
      "type": "http",
      "url": "https://mcp.fireslide.ai/"
    }
  }
}
```

## Compatibility

- Codex: use this plugin repo.
- Claude Code: connect directly to `https://mcp.fireslide.ai/`.
- Other MCP clients: use the `.mcp.json` shape above if they support remote HTTP MCP servers with OAuth.

## Usage Examples

Ask Codex:

```text
Create a 6-slide executive briefing on the latest AI news today.
```

```text
Build a seed-stage pitch deck for an AI sales copilot called Signal AI.
```

```text
Turn these notes into a clean proposal deck and render it in Fireslide.
```

## Security Model

This plugin is intentionally thin. Users can inspect this repository, but the real Fireslide implementation runs on the hosted Fireslide service.

Do not add private backend files, provider credentials, service-account files, or proprietary source code to this repo.

## Support

Website: https://fireslide.ai

Privacy policy: https://fireslide.ai/privacy

Contact: support@fireslide.ai
