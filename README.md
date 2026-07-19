# Fireslide Codex Plugin

Fireslide is a Codex plugin and MCP setup for creating editable presentation decks through the hosted Fireslide MCP server.

It lets Codex discover the live Fireslide capabilities, choose styles, import user-provided images into deck assets, render editable decks, and return a Fireslide editor URL.
It also guides Codex to revise an existing Fireslide deck in place when the user provides a Fireslide editor URL or presentation id.

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

Recommended setup is to add this repository as a Codex plugin marketplace, then install the Fireslide plugin from that marketplace.

First, make sure your Codex CLI exposes plugin install commands:

```bash
codex plugin --help
```

You should see `add`, `list`, `marketplace`, and `remove`. If `add` is missing, update Codex first:

```bash
codex update
```

Then add the Fireslide marketplace:

```bash
codex plugin marketplace add FireSlideAI/fireslide-plugin
```

Confirm Codex can see the plugin:

```bash
codex plugin list --marketplace fireslide
```

Install Fireslide:

```bash
codex plugin add fireslide@fireslide
```

Start a new Codex thread after installing so Codex loads the Fireslide skill and MCP tools. If you prefer the app UI, open Plugins, choose the Fireslide marketplace, and install Fireslide there.

For local development from a clone:

```bash
codex plugin marketplace add /absolute/path/to/fireslide-plugin
```

Then install Fireslide from the local marketplace:

```bash
codex plugin add fireslide@fireslide
```

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

## Live MCP Contract

The hosted server is the canonical source for the current tool set and schemas. Discover its live capabilities before acting; this setup plugin intentionally does not maintain a fixed catalog.

For new decks, retrieve a compact style view first, then request only selected layouts. For existing decks, read an outline before requesting selected slide detail, and edit stable slide IDs with the returned state token. Imported layouts may expose a `patches` contract: target only approved stable element IDs and permitted fields, preserving every unmentioned layout element and content.

Choose the asset route that the host can support: URL import, base64 upload, or direct upload. The live direct-upload capability returns a short-lived single-use signed upload_url; use it only when the host can POST a local file. POST the raw local file as multipart field `image`, then use the durable asset `url` from that upload response. Visual and research helpers are optional live capabilities; a media failure must not prevent rendering. Return the exact full Fireslide `view_url` or editor URL from the render or edit result.

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
