from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    line: int  # 1-based


@dataclass(frozen=True)
class CodeBlock:
    info: str
    content: str
    start_line: int  # 1-based
    end_line: int  # 1-based


_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    return _NORMALIZE_RE.sub(" ", text).strip()


def parse_markdown(content: str) -> Dict[str, object]:
    """Parse Markdown and return a context dict used by rules.

    Uses markdown-it-py for reliable tokenization and line mappings.
    Core engine and rules should treat this as an input contract.
    """
    md = MarkdownIt("commonmark").enable("strikethrough")
    tokens = md.parse(content)

    lines = content.splitlines()
    headings: List[Heading] = []
    code_blocks: List[CodeBlock] = []

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.type == "heading_open":
            level = int(tok.tag[1:]) if tok.tag.startswith("h") else 0
            # map is [start_line, end_line) 0-based
            start_line = (tok.map[0] + 1) if tok.map else 1
            inline = tokens[i + 1] if i + 1 < len(tokens) else None
            text = inline.content if inline and inline.type == "inline" else ""
            headings.append(Heading(level=level, text=text, line=start_line))
            i += 1
        elif tok.type == "fence":
            start_line = (tok.map[0] + 1) if tok.map else 1
            end_line = (tok.map[1]) if tok.map else start_line
            code_blocks.append(CodeBlock(info=tok.info or "", content=tok.content or "", start_line=start_line, end_line=end_line))
        i += 1

    # Build section ranges for headings (only ## and deeper are considered sections for this tool).
    # Each section is (heading, start_line, end_line) in 1-based inclusive start, inclusive end.
    section_ranges: List[Tuple[Heading, int, int]] = []
    relevant = [h for h in headings if h.level >= 2]
    # sort by line already
    for idx, h in enumerate(relevant):
        start = h.line
        end = len(lines)
        if idx + 1 < len(relevant):
            end = max(1, relevant[idx + 1].line - 1)
        section_ranges.append((h, start, end))

    return {
        "lines": lines,
        "headings": headings,
        "code_blocks": code_blocks,
        "section_ranges": section_ranges,
    }


def find_section(
    context: Dict[str, object],
    keywords: List[str],
    *,
    min_level: int = 2,
) -> Optional[Tuple[Heading, int, int]]:
    """Find the first section whose normalized heading contains any keyword."""
    section_ranges = context.get("section_ranges", [])
    for h, start, end in section_ranges:
        if h.level < min_level:
            continue
        norm = normalize_heading(h.text)
        for kw in keywords:
            if kw in norm:
                return (h, start, end)
    return None


def iter_sections(context: Dict[str, object]) -> List[Tuple[Heading, int, int]]:
    return list(context.get("section_ranges", []))
