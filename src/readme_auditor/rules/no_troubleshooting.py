from __future__ import annotations

from typing import Dict, List

from ..models import Issue, RuleMeta
from ..parser import find_section
from .base import Rule


class NoTroubleshootingRule(Rule):
    meta = RuleMeta(
        rule_id="no_troubleshooting",
        name="Missing troubleshooting section",
        severity="info",
        description="Checks for Troubleshooting, FAQ, or Common Issues section.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        section = find_section(context, ["troubleshooting", "faq", "common issues", "common problems"])
        if section:
            return []
        return [
            Issue(
                rule_id=self.id,
                severity=self.severity,
                line=None,
                text="No troubleshooting section",
                explanation="Readers often need quick fixes for setup or usage issues.",
                suggestion="Add '## Troubleshooting' with at least two common failure cases and fixes.",
            )
        ]
