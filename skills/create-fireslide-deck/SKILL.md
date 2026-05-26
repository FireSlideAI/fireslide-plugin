---
name: create-fireslide-deck
description: Use when the user asks Codex to create, design, revise, render, or export a presentation, slide deck, slides, PowerPoint, PPTX, proposal, briefing, pitch deck, or visual report through Fireslide.
---

# Create Fireslide Deck

Use the hosted Fireslide MCP server to create editable presentation decks that open in the Fireslide editor.

## Core Workflow

1. Treat normal presentation requests as deck creation requests.
   - Examples: "make a deck", "help me create slides", "turn this into a presentation", "build a pitch deck", "make an executive briefing".
   - Ask a clarifying question only when a missing answer materially changes the deck.
   - Otherwise infer slide count, audience, language, and tone from the prompt.

2. Pick a visual system.
   - Call `list_styles` with the user's topic, audience, and style intent.
   - Choose the closest style returned by the server.
   - Call `get_style` for the selected style before authoring slides.
   - Prefer a lightweight first call to inspect available subtype keys, then request only the subtype templates needed for the deck when the tool supports that mode.

3. Author against the returned style contract.
   - Use only `sub_type` values returned by `get_style`.
   - Prefer returned templates and mutate text, image URLs, colors, and layout.
   - Prefer `fill` when a returned `fill_schema` exists.
   - Use explicit `elements` when freeform layout control is needed.

4. Use media and research tools intentionally.
   - `search_news`: current events, recent company news, daily briefings, market updates.
   - `search_images`: real photos, products, places, people, logos, screenshots.
   - `generate_image`: bespoke illustrations or scenes.
   - `make_svg`: one transparent hero cutout or object on a colored background.
   - `make_meme`: humor, meme recaps, or lightweight interstitial slides.

5. Render.
   - Call `render_presentation` with `user_input`, `style_name`, `title`, and complete `slides`.
   - Return the `view_url` to the user.
   - Tell the user the deck can be edited and exported from Fireslide.

## Current News

For prompts mentioning latest, today, current, recent, news, this week, market update, industry update, company update, or daily briefing:

1. Call `search_news` before drafting.
2. Use returned article titles, source domains, snippets, dates, and images as source material.
3. Do not invent fresh headlines, quotes, dates, or exact statistics.
4. If `search_news` fails or is quota-limited, tell the user and retry once with a simpler query.

## Freeform Element Rules

When authoring explicit elements:

- Fireslide uses a 1280x720 pixel canvas.
- `x`, `y`, `w`, and `h` are absolute pixels.
- Good values look like `x:80`, `y:96`, `w:1120`, `h:90`.
- Never use grid or inch-like values such as `x:1`, `y:2`, `w:10`, `h:1.5`.
- Every slide must include `slide_meta` with `width:1280`, `height:720`, and a hex `background`.
- Every element must include `id`, `type`, `x`, `y`, `w`, `h`, and `z`.
- Element properties are flat at the element root. Do not nest visual fields under `style`, `props`, `attributes`, or `data`.
- Use snake_case fields such as `font_size`, `font_weight`, `font_family`, and `line_height`.
- Use returned image URLs in image element `src` fields. Do not invent image URLs.

Common element fields:

- `text`: `text`, `font_family`, `font_size`, `font_weight`, `color`, `align`, `line_height`
- `image`: `src`, `fit`, `radius`
- `shape`: `shape`, `fill`, `opacity`, `radius`, `points`
- `icon`: `icon`, `style`, `color`, `font_size`
- `mermaid`: `source`
- `chart`: `engine`, `option`

## Quality Bar

- One main idea per slide.
- Prefer fewer, stronger slides over crowded layouts.
- Keep text readable and inside its boxes.
- Use generous margins.
- Follow user-specified colors, copy, typography, language, and slide-by-slide instructions exactly.
- Do not add decorative graphics, stock photos, gradients, or extra sections unless requested.
- If a paid media tool returns a quota or upgrade error, continue with text, simple shapes, or placeholders and explain the limitation briefly.

## User-Facing Result

After rendering, respond with:

- deck title
- one-sentence summary of what was created
- Fireslide editor URL
- any media, search, or quota limitations encountered
