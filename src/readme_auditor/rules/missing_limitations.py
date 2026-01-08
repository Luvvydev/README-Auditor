from __future__ import annotations

from typing import Dict, List

from ..models import Issue, RuleMeta
from ..parser import find_section
from .base import Rule


class MissingLimitationsRule(Rule):
    meta = RuleMeta(
        rule_id="missing_limitations",
        name="Missing limitations section",
        severity="warning",
        description="Checks for Limitations, Non-goals, or Known Issues section.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        section = find_section(context, ["limitations", "non goals", "non-goals", "known issues", "caveats"])
        if section:
            return []
        return [
            Issue(
                rule_id=self.id,
                severity=self.severity,
                line=None,
                text="No limitations section",
                explanation="Without limitations, readers may assume capabilities that are not supported.",
                suggestion="Add '## Limitations' or '## Non-goals' describing what the project does not cover.",
            )
        ]
