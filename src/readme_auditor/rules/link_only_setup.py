from __future__ import annotations

import re
from typing import Dict, List

from ..models import Issue, RuleMeta
from ..parser import find_section
from .base import Rule


_LINK = re.compile(r"https?://\S+", re.IGNORECASE)
_DOC_PHRASES = re.compile(r"\b(see|read|refer\s+to)\s+(the\s+)?(docs|documentation|guide)\b", re.IGNORECASE)


class LinkOnlySetupRule(Rule):
    meta = RuleMeta(
        rule_id="link_only_setup",
        name="Link-only setup",
        severity="warning",
        description="Flags installation sections that only point to external docs without concrete steps.",
    )

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        code_blocks = context["code_blocks"]
        section = find_section(context, ["installation", "setup", "getting started"])
        if not section:
            return []
        heading, start, end = section
        lines = context["lines"]
        body = "\n".join(lines[start - 1 : end])

        has_link = bool(_LINK.search(body)) and bool(_DOC_PHRASES.search(body))
        has_code = any((cb.start_line >= start and cb.end_line <= end) for cb in code_blocks)

        if has_link and not has_code:
            return [
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=heading.line,
                    text=heading.text,
                    explanation="Installation points to external documentation but provides no concrete commands or steps.",
                    suggestion="Add minimal, copy-pasteable installation commands directly in the README.",
                )
            ]
        return []
