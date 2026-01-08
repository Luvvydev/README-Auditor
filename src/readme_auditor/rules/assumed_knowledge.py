from __future__ import annotations

import re
from typing import Dict, List

from ..models import Issue, RuleMeta
from ..parser import find_section
from ._utils import iter_matching_lines
from .base import Rule


_IMPERATIVE = re.compile(r"\b(just|simply)\s+run\b|\brun\s+make\b|\bcd\s+\S+\s*&&\s*make\b|\bdo\s+this\b", re.IGNORECASE)
_PREREQ = re.compile(r"\b(prereq|requirements?|depends\s+on|requires)\b", re.IGNORECASE)


class AssumedPriorKnowledgeRule(Rule):
    meta = RuleMeta(
        rule_id="assumed_knowledge",
        name="Assumed prior knowledge",
        severity="info",
        description="Flags imperative setup steps that omit prerequisites or context.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lines = context["lines"]
        install = find_section(context, ["installation", "setup", "getting started"])
        if not install:
            return []
        heading, start, end = install
        body_lines = lines[start - 1 : end]

        issues: List[Issue] = []
        has_prereq_section = bool(_PREREQ.search("\n".join(body_lines)))
        for lineno, line, _ in iter_matching_lines(lines, _IMPERATIVE, start_line=start, end_line=end):
            if has_prereq_section:
                continue
            issues.append(
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=lineno,
                    text=line.strip(),
                    explanation="Setup instruction assumes tools or context that may not be installed or understood.",
                    suggestion="State prerequisites (Python version, OS, tools) and explain what the command does.",
                )
            )
        return issues
