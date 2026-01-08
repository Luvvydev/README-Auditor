from __future__ import annotations

from readme_auditor.parser import find_section, iter_sections, parse_markdown


def test_find_section_returns_none_when_missing():
    ctx = parse_markdown("# T\n\n## Alpha\n\nText\n")
    assert find_section(ctx, ["installation"]) is None


def test_iter_sections_returns_ranges():
    ctx = parse_markdown("# T\n\n## A\n\nText\n\n## B\n\nText\n")
    sections = iter_sections(ctx)
    assert len(sections) == 2
    h1, s1, e1 = sections[0]
    assert h1.text == "A"
    assert s1 <= e1


def test_find_section_respects_min_level():
    ctx = parse_markdown("# T\n\n## Installation\n\nText\n\n### Deep\n\nText\n")
    # min_level=3 should skip the level-2 Installation heading
    assert find_section(ctx, ["installation"], min_level=3) is None
