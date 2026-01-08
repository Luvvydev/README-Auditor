from __future__ import annotations

import re
from typing import Iterable, List, Optional, Tuple


def iter_matching_lines(
    lines: List[str],
    pattern: re.Pattern[str],
    *,
    start_line: int = 1,
    end_line: Optional[int] = None,
) -> Iterable[Tuple[int, str, re.Match[str]]]:
    if end_line is None:
        end_line = len(lines)
    for lineno in range(start_line, end_line + 1):
        if lineno < 1 or lineno > len(lines):
            continue
        text = lines[lineno - 1]
        m = pattern.search(text)
        if m:
            yield lineno, text, m
