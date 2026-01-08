from __future__ import annotations

import re
from typing import Dict, List

from ..models import Issue, RuleMeta
from ._utils import iter_matching_lines
from .base import Rule


_OVERPROMISE = re.compile(
    r"\b(everything\s+you\s+need\b|complete\s+solution\b|one\s+tool\s+to\s+rule\s+them\s+all\b|solves\s+all\b|works\s+for\s+any\b)\b",
    re.IGNORECASE,
)
_BOUNDS = re.compile(r"\b(limited\s+to|only\s+for|for\s+this\s+use\s+case|in\s+this\s+project)\b", re.IGNORECASE)


class OverpromisingScopeRule(Rule):
    meta = RuleMeta(
        rule_id="overpromising",
        name="Overpromising scope",
        severity="warning",
        description="Flags universal claims about scope without constraints.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lines = context["lines"]
        issues: List[Issue] = []
        for lineno, line, match in iter_matching_lines(lines, _OVERPROMISE):
            if _BOUNDS.search(line):
                continue
            issues.append(
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=lineno,
                    text=line.strip(),
                    explanation="Scope claim uses universal language without stating constraints or non-goals.",
                    suggestion="Replace universal claims with bounded scope and link to Limitations or Non-goals.",
                )
            )
        return issues
