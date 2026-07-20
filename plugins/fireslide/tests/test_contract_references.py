from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_SOURCES = {
    "README": REPO_ROOT / "README.md",
    "deck skill": REPO_ROOT
    / "plugins"
    / "fireslide"
    / "skills"
    / "create-fireslide-deck"
    / "SKILL.md",
    "MCP config": REPO_ROOT / "plugins" / "fireslide" / ".mcp.json",
}
RETIRED_TOOL_NAMES = ("show_deck_preview", "make_meme", "search_memes")
CATALOG_CLAIM_PATTERN = re.compile(
    r"(?im)\btools?\s+include\b"
    r"|\bexposes\s+the\s+following\s+tools\b"
    r"|\b(?:offers|exposes|includes|has)\s+\d+\s+(?:mcp\s+)?tools?\b"
)
CATALOG_HEADING_PATTERN = re.compile(
    r"(?im)^#{1,6}\s+[^\n]*\b(?:tools?|catalog|inventory|capabilit(?:y|ies))\b"
)
CATALOG_BULLET_PATTERN = re.compile(
    r"(?im)^[ \t]*[-*+]\s+`?[a-z][a-z0-9]*(?:_[a-z0-9]+)+`?(?:\s*(?::|[-—])|\s*$)"
)


def read_contract_sources():
    return {
        source_name: source_path.read_text(encoding="utf-8").lower()
        for source_name, source_path in CONTRACT_SOURCES.items()
    }


def has_catalog_reference(contents):
    return any(
        pattern.search(contents)
        for pattern in (
            CATALOG_CLAIM_PATTERN,
            CATALOG_HEADING_PATTERN,
            CATALOG_BULLET_PATTERN,
        )
    )


def test_setup_sources_do_not_reference_retired_tools():
    for source_name, contents in read_contract_sources().items():
        for tool_name in RETIRED_TOOL_NAMES:
            assert tool_name not in contents, f"{source_name} references retired {tool_name}"


def test_each_setup_source_defers_to_live_discovery_without_a_catalog():
    for source_name, contents in read_contract_sources().items():
        assert "live" in contents, f"{source_name} must defer to live discovery"
        assert "discover" in contents, f"{source_name} must tell Codex to discover"
        assert "canonical" in contents, f"{source_name} must name the server canonical"
        assert not has_catalog_reference(contents), (
            f"{source_name} claims a fixed tool catalog"
        )


def test_readme_and_skill_preserve_imported_patch_contract():
    for source_name in ("README", "deck skill"):
        contents = read_contract_sources()[source_name]
        assert "patches" in contents
        assert "approved stable element ids" in contents
        assert "permitted fields" in contents
        assert "unmentioned layout element" in contents


def test_readme_and_skill_explain_signed_direct_upload():
    for source_name in ("README", "deck skill"):
        contents = read_contract_sources()[source_name]
        assert "short-lived single-use signed upload_url" in contents
        assert "post a local file" in contents
        assert "multipart field `image`" in contents
        assert "durable asset `url`" in contents


@pytest.mark.parametrize(
    "bad_snippet",
    (
        "## Live MCP Contract\n\n- list_styles\n- `get_style`\n"
        "- render_presentation: creates a deck\n- get_deck\n- edit_deck",
        "## Available Capabilities\n\nDiscover live schemas before acting.",
    ),
)
def test_catalog_guard_rejects_structural_catalog_snippets(bad_snippet):
    assert has_catalog_reference(bad_snippet)


@pytest.mark.parametrize(
    "normal_bullet",
    (
        "- URL route: import a temporary attachment URL.",
        "- Base64 route: upload image bytes.",
        "- Direct-upload route: POST a local file.",
        "- Keep one main idea per slide.",
    ),
)
def test_catalog_guard_allows_normal_workflow_bullets(normal_bullet):
    assert not has_catalog_reference(normal_bullet)
