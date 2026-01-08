from __future__ import annotations

import re
from typing import Dict, List

from ..models import Issue, RuleMeta
from ._utils import iter_matching_lines
from .base import Rule


_ABSOLUTES = re.compile(
    r"\b(never\s+crash(?:es|ed)?|always\s+work(?:s|ed)?|100%\s+reliable|guarantee(?:d)?\s+to\s+work|zero\s+bugs)\b",
    re.IGNORECASE,
)
_CAVEAT = re.compile(r"\b(most|usually|often|typically|best\s+effort|may|might|can)\b", re.IGNORECASE)


class UnfalsifiableClaimsRule(Rule):
    meta = RuleMeta(
        rule_id="unfalsifiable",
        name="Unfalsifiable claims",
        severity="warning",
        description="Flags absolute language that cannot be realistically guaranteed.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lines = context["lines"]
        issues: List[Issue] = []
        for lineno, line, match in iter_matching_lines(lines, _ABSOLUTES):
            if _CAVEAT.search(line):
                continue
            phrase = match.group(0)
            issues.append(
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=lineno,
                    text=line.strip(),
                    explanation=f"Absolute phrase {phrase!r} is not realistically falsifiable or supportable in a README.",
                    suggestion="Replace absolutes with bounded claims and describe known failure modes or constraints.",
                )
            )
        return issues
