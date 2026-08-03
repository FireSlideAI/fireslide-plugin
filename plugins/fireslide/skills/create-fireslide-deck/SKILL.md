---
name: create-fireslide-deck
description: Use when the user asks Codex to create, design, revise, render, or export a presentation, slide deck, slides, PowerPoint, PPTX, proposal, briefing, pitch deck, or visual report through Fireslide.
---

# Create Fireslide Deck

Use the hosted Fireslide MCP server to create and revise editable presentation decks. This plugin supplies Codex workflow glue; live server discovery and tool schemas are always canonical.

## Start With Live Discovery

Before acting, inspect the live tools and schemas available from the Fireslide server. Do not assume a fixed tool count or reproduce a tool catalog here. Select only capabilities that the live server exposes and that the user's request needs.

Ask a short clarifying question only when missing audience, goal, tone, slide count, source material, language, or output would materially change the deck. Otherwise infer those basics from the request.

## Route Layout Intent

A source layout is optional: normal fresh deck creation uses the selected target style's full layouts or a flexible/default authoring path. Route on intent before the presence of a named source: inspiration, similarity, or idea requests always take precedence, even when the user also names a specific external slide or layout. For those requests, create a new composition inspired by the source in the target style. Use faithful transfer only when a specific external slide or layout is named without inspiration, similarity, or idea intent. Without inspiration, similarity, or idea intent, requests to copy, reproduce, preserve, or match the named source exactly use faithful transfer. A selected imported layout may use manifest detail for its faithful copy-and-patch path. For cross-style requests, retrieve source manifest detail only for faithful transfer; never retrieve it for the inspiration route. Use the live render or edit schema for faithful transfer. The live server schema remains canonical.

## Create a Deck

1. Discover the live style capability and choose a style appropriate to the request.
2. Call `get_style` for the selected style without layouts first. Use that compact response to choose layout keys, then call `get_style` again for only the selected layouts in small batches. Follow any selection or response-size guidance returned by the live schema.
3. Author only against the returned style contract. If a selected imported layout exposes a `patches` contract, target only approved stable element IDs and permitted fields, preserving every unmentioned layout element and content rather than rebuilding the layout.
4. Use the live render capability with the selected style and completed slides.
5. Review the affected rendered slides as described in **Review the Result**, then return the exact full Fireslide `view_url` or editor URL from the write result.

## Revise an Existing Deck

1. Identify the existing deck from the supplied editor URL, presentation ID, or a prior result in this conversation.
2. Call `get_deck` in outline mode first. It provides stable slide IDs and the current state token without retrieving unnecessary slide material.
3. Call `get_deck` again only for selected slide IDs when the requested change needs slide detail. Target edits by stable slide ID and send the latest returned state token with the change.
4. Make the smallest change that satisfies the request. When faithful transfer was selected under Route Layout Intent, preserve the live edit schema's `slide.transfer` route when applicable. If the server reports a changed deck state, refetch the outline and selected slides, rebuild against the latest IDs and state token, and retry once.
5. Review the affected rendered slides as described in **Review the Result**.
6. Return the exact full Fireslide `view_url` or editor URL from the edit result.

## Review the Result

After every successful render or edit, use the live review capability when the server exposes it and the write result requests review. Pass the write result's presentation ID as the deck ID, its latest state token, and only its returned review slide IDs. Review only the affected slides; this keeps a one-slide edit focused on that slide instead of reviewing the whole deck.

Follow the returned next cursor until the affected set is complete. Inspect every individual slide image, not only a combined thumbnail or contact sheet, and use the returned deterministic findings as review hints. Check for clipping, overlap, unreadably small text, weak hierarchy, unintended template changes, and inconsistent spacing. If review reveals a clear problem, make the smallest corrective edit and review the changed slides again.

Review is quality assurance, not a second deck write and not a replacement for the human editor preview. If review rendering fails, do not recreate the deck. Return the original editor URL and briefly report that automated visual review was unavailable.

## Assets, Media, and Research

Choose the asset route supported by the current host and live schema:

- URL route: import an attachment when the host exposes a temporary or public URL, then use the returned durable asset URL.
- Base64 route: upload image bytes when the host can provide base64, then use the returned durable asset URL.
- Direct-upload route: the live capability returns a short-lived single-use signed upload_url. Use it only when the host can POST a local file; POST the raw local file as multipart field `image`, then use the durable asset `url` from that upload response.

Visual and research helpers are optional capabilities discovered from the live server. Use them only when their result will improve the deck. If a visual or research call fails, is unavailable, or is quota-limited, continue rendering with the available content and briefly state the limitation.

## Quality Bar

- Keep one main idea per slide and make content readable with sufficient margins.
- Follow the requested copy, language, and style.
- Do not add unrequested decoration or sections.

## User-Facing Result

Tell the user what was created or revised, note any media or review limitation, and return the exact full Fireslide `view_url` or editor URL. The deck remains editable and exportable in Fireslide.
