from __future__ import annotations

from typing import Dict, List

from ..models import Issue, RuleMeta
from ..parser import find_section, normalize_heading
from .base import Rule


class NoExamplesRule(Rule):
    meta = RuleMeta(
        rule_id="no_examples",
        name="Missing input or output examples",
        severity="warning",
        description="Checks that Usage or Examples includes at least one code block.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        lines = context["lines"]
        code_blocks = context["code_blocks"]
        section = find_section(context, ["usage", "examples"])
        if not section:
            return [
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=None,
                    text="No Usage or Examples section found",
                    explanation="Without examples, readers cannot quickly understand expected input and output.",
                    suggestion="Add '## Usage' or '## Examples' with at least one runnable command.",
                )
            ]

        heading, start, end = section

        has_code = any((cb.start_line >= start and cb.end_line <= end) for cb in code_blocks)
        if has_code:
            return []

        snippet = ""
        if start <= len(lines):
            snippet = lines[start - 1].strip()

        return [
            Issue(
                rule_id=self.id,
                severity=self.severity,
                line=start,
                text=snippet or heading.text,
                explanation="Usage or Examples section has no code blocks showing real input or output.",
                suggestion="Include at least one command-line invocation and its expected output.",
            )
        ]
