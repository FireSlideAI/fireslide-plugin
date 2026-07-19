from pathlib import Path
import re


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


def test_setup_sources_do_not_reference_retired_tools():
    for source_name, source_path in CONTRACT_SOURCES.items():
        contents = source_path.read_text(encoding="utf-8")
        for tool_name in RETIRED_TOOL_NAMES:
            assert tool_name not in contents, f"{source_name} references retired {tool_name}"


def test_setup_sources_defer_to_live_tool_discovery():
    combined_contents = "\n".join(
        source_path.read_text(encoding="utf-8")
        for source_path in CONTRACT_SOURCES.values()
    ).lower()

    assert not re.search(
        r"\b(?:offers|exposes|includes|has)\s+\d+\s+(?:mcp\s+)?tools?\b",
        combined_contents,
    )
    assert "## main tools" not in combined_contents
    assert "live" in combined_contents and "discover" in combined_contents
