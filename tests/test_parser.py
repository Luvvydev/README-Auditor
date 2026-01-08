from __future__ import annotations

from readme_auditor.parser import find_section, parse_markdown


def test_parse_headings_and_sections():
    md = "# Title\n\n## Installation\n\nDo this\n\n## Usage\n\n```bash\ncmd\n```\n"
    ctx = parse_markdown(md)
    headings = ctx["headings"]
    assert any(h.text == "Installation" and h.level == 2 for h in headings)
    sec = find_section(ctx, ["installation"])
    assert sec is not None
    h, start, end = sec
    assert h.text == "Installation"
    assert start >= 1
    assert end >= start
