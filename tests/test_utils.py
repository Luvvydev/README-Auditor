from __future__ import annotations

import re

from readme_auditor.rules._utils import iter_matching_lines


def test_iter_matching_lines_end_line_none_uses_full_length():
    lines = ["one", "two match", "three"]
    pat = re.compile(r"match")
    matches = list(iter_matching_lines(lines, pat, start_line=1, end_line=None))
    assert matches and matches[0][0] == 2


def test_iter_matching_lines_skips_out_of_bounds_lines():
    lines = ["match"]
    pat = re.compile(r"match")
    # start_line 0 produces an out of bounds lineno (0) and end_line beyond length
    matches = list(iter_matching_lines(lines, pat, start_line=0, end_line=3))
    assert matches and matches[0][0] == 1
