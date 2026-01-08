from __future__ import annotations

from typing import Dict, List

from ..models import Issue, RuleMeta
from .base import Rule


class UnclearAudienceRule(Rule):
    meta = RuleMeta(
        rule_id="unclear_audience",
        name="Unclear audience",
        severity="info",
        description="Checks whether the README clearly states the target audience and artifact type.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lowered = content.lower()
        mentions = [
            "cli",
            "command line",
            "library",
            "python package",
            "github action",
            "framework",
            "tool",
        ]
        has_statement = any(m in lowered for m in mentions)
        if has_statement:
            return []
        return [
            Issue(
                rule_id=self.id,
                severity=self.severity,
                line=1,
                text=(context["lines"][0].strip() if context.get("lines") else ""),
                explanation="README does not clearly state whether this is a CLI tool, library, or something else.",
                suggestion="Add a short sentence near the top stating the audience and usage mode.",
            )
        ]
