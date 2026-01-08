from __future__ import annotations

import re
from typing import Dict, List

from ..models import Issue, RuleMeta
from ._utils import iter_matching_lines
from .base import Rule

DEFAULT_ADJECTIVES = ["fast", "simple", "powerful", "scalable"]

_WORD = r"\b({words})\b"
_NUMERIC_EVIDENCE = re.compile(r"\b(\d+(?:\.\d+)?%?|ms|s|sec|seconds|x|times|bench(?:mark)?|compare|vs\.?|p\d{2,}|v\d+\.\d+)\b", re.IGNORECASE)


class VagueClaimsRule(Rule):
    meta = RuleMeta(
        rule_id="vague_claims",
        name="Vague claims detector",
        severity="warning",
        description="Flags vague adjectives like 'fast' or 'simple' when not supported by evidence.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lines = context["lines"]
        custom = self.options.get("custom_adjectives")
        adjectives = list(DEFAULT_ADJECTIVES)
        if isinstance(custom, list):
            adjectives.extend([str(x).strip() for x in custom if str(x).strip()])

        words = "|".join(re.escape(a) for a in sorted(set(adjectives), key=len, reverse=True))
        pattern = re.compile(_WORD.format(words=words), re.IGNORECASE)

        issues: List[Issue] = []
        for lineno, line, match in iter_matching_lines(lines, pattern):
            # Require absence of numeric evidence on same line and nearby (one line forward)
            window = line
            if lineno < len(lines):
                window += " " + lines[lineno]
            if _NUMERIC_EVIDENCE.search(window):
                continue

            word = match.group(0)
            issues.append(
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=lineno,
                    text=line.strip(),
                    explanation=f"Adjective {word!r} lacks evidence or context (numbers, benchmarks, or comparisons).",
                    suggestion="Add benchmarks, comparisons, or specific examples that justify the claim.",
                )
            )
        return issues
