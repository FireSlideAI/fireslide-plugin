---
name: create-fireslide-deck
description: Use when the user asks Codex to create, design, revise, render, or export a presentation, slide deck, slides, PowerPoint, PPTX, proposal, briefing, pitch deck, or visual report through Fireslide.
---

# Create Fireslide Deck

Use the hosted Fireslide MCP server to create and revise editable presentation decks. This plugin supplies Codex workflow glue; live server discovery and tool schemas are always canonical.

## Start With Live Discovery

Before acting, inspect the live tools and schemas available from the Fireslide server. Do not assume a fixed tool count or reproduce a tool catalog here. Select only capabilities that the live server exposes and that the user's request needs.

Ask a short clarifying question only when missing audience, goal, tone, slide count, source material, language, or output would materially change the deck. Otherwise infer those basics from the request.

## Create a Deck

1. Discover the live style capability and choose a style appropriate to the request.
2. Call `get_style` for the selected style without layouts first. Use that compact response to choose layout keys, then call `get_style` again for only the selected layouts in small batches. Follow any selection or response-size guidance returned by the live schema.
3. Author only against the returned style contract. If a selected imported layout exposes a `patches` contract, preserve the layout and use those patches rather than rebuilding its elements.
4. Use the live render capability with the selected style and completed slides. Return the exact full Fireslide `view_url` or editor URL that it returns.

## Revise an Existing Deck

1. Identify the existing deck from the supplied editor URL, presentation ID, or a prior result in this conversation.
2. Call `get_deck` in outline mode first. It provides stable slide IDs and the current state token without retrieving unnecessary slide material.
3. Call `get_deck` again only for selected slide IDs when the requested change needs slide detail. Target edits by stable slide ID and send the latest returned state token with the change.
4. Make the smallest change that satisfies the request. If the server reports a changed deck state, refetch the outline and selected slides, rebuild against the latest IDs and state token, and retry once.
5. Return the exact full Fireslide `view_url` or editor URL from the edit result.

## Assets, Media, and Research

Choose the asset route supported by the current host and live schema:

- URL route: import an attachment when the host exposes a temporary or public URL, then use the returned durable asset URL.
- Base64 route: upload image bytes when the host can provide base64, then use the returned durable asset URL.
- Direct-upload route: use a host-provided direct upload when available, then use its returned durable asset URL.

Visual and research helpers are optional capabilities discovered from the live server. Use them only when their result will improve the deck. If a visual or research call fails, is unavailable, or is quota-limited, continue rendering with the available content and briefly state the limitation.

## User-Facing Result

Tell the user what was created or revised, note any media limitation, and return the exact full Fireslide `view_url` or editor URL. The deck remains editable and exportable in Fireslide.
