# Fireslide Codex Plugin

Fireslide is a Codex plugin and MCP setup for creating editable presentation decks through the hosted Fireslide MCP server.

It lets Codex choose Fireslide styles, use deck-specific media and news tools, render editable decks, show deck preview metadata on compatible hosts, and return a Fireslide editor URL.

The plugin does not include the Fireslide backend or renderer. It only packages Codex metadata, a deck-creation skill, and a remote MCP server config for the hosted Fireslide service.

## What This Repo Contains

- A Codex marketplace at `.agents/plugins/marketplace.json`
- The Fireslide plugin at `plugins/fireslide`
- Codex plugin metadata at `plugins/fireslide/.codex-plugin/plugin.json`
- Remote MCP config at `plugins/fireslide/.mcp.json`
- A Codex skill that teaches the deck-creation workflow

## What This Repo Does Not Contain

- Fireslide backend source code
- Renderer implementation
- Style catalog internals
- Auth service code
- API keys or secrets
- Paid media/news provider credentials

All proprietary product logic stays behind the hosted Fireslide MCP service.

## Hosted MCP Server

The plugin connects to the hosted Streamable HTTP MCP endpoint:

```text
https://mcp.fireslide.ai
```

On first use, Codex authenticates through Fireslide OAuth. Do not use `https://mcp.fireslide.ai/sse`; that path is not the current Codex endpoint.

## Install In Codex

Recommended setup is to add this repository as a Codex plugin marketplace, then install the Fireslide plugin from Codex's plugin UI.

```bash
codex plugin marketplace add FireSlideAI/fireslide-plugin
```

Then open Codex, go to Plugins, choose the Fireslide marketplace, and install Fireslide. Start a new thread after installing so Codex loads the skill and MCP tools.

For local development from a clone:

```bash
codex plugin marketplace add /absolute/path/to/fireslide-plugin
```

Then install Fireslide from the local marketplace in the Codex plugin UI and start a new thread.

## Direct MCP Fallback

If you only need the hosted Fireslide MCP tools and do not need the Codex plugin skill, register the server directly:

```bash
codex mcp add fireslide --url https://mcp.fireslide.ai
codex mcp login fireslide
```

Equivalent `~/.codex/config.toml`:

```toml
[mcp_servers.fireslide]
url = "https://mcp.fireslide.ai"
```

Direct MCP exposes the tools, but it does not install the `create-fireslide-deck` skill or plugin metadata. For normal users, prefer the plugin marketplace setup.

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

`render_presentation` returns an editor URL and structured deck preview metadata. Hosts that support MCP app widgets may render an inline deck preview; other hosts should still show the text response and editor URL.

## Claude Code

Claude Code does not use the Codex plugin wrapper. Connect it directly to the hosted MCP server:

```bash
claude mcp add --transport http fireslide https://mcp.fireslide.ai
```

On first use, Claude Code should open the Fireslide OAuth flow. After auth, the same hosted MCP tools are available, but the Codex-specific skill is not installed.

## Claude Desktop And Other MCP Clients

Use a remote HTTP MCP server config if your client supports remote MCP with OAuth:

```json
{
  "mcpServers": {
    "fireslide": {
      "type": "http",
      "url": "https://mcp.fireslide.ai"
    }
  }
}
```

Widget rendering is host-dependent. Treat the Fireslide editor URL as the stable fallback across clients.

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
