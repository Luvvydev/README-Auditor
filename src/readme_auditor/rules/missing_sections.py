from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from ..models import Issue, RuleMeta
from ..parser import normalize_heading
from .base import Rule


class MissingRequiredSectionsRule(Rule):
    meta = RuleMeta(
        rule_id="missing_sections",
        name="Missing required sections",
        severity="warning",
        description="Checks for common README sections such as Installation and Usage.",
    )

    def _has_section(self, headings: List[object], keyword: str) -> bool:
        for h in headings:
            text = getattr(h, "text", "")
            level = getattr(h, "level", 0)
            if level < 2:
                continue
            if keyword in normalize_heading(str(text)):
                return True
        return False

    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        headings = context["headings"]
        # Defaults and config overrides
        required = ["installation", "usage", "license"]
        optional = ["contributing"]
        opt_cfg = self.options.get("optional")
        req_cfg = self.options.get("required")
        if isinstance(req_cfg, list):
            required = [str(x).strip().lower() for x in req_cfg if str(x).strip()]
        if isinstance(opt_cfg, list):
            optional = [str(x).strip().lower() for x in opt_cfg if str(x).strip()]

        issues: List[Issue] = []

        for kw in required:
            if not self._has_section(headings, kw):
                sev = "error" if kw in {"installation", "usage"} else self.severity
                issues.append(
                    Issue(
                        rule_id=self.id,
                        severity=sev,  # type: ignore[arg-type]
                        line=None,
                        text=f"Missing section: {kw}",
                        explanation=f"README is missing a '## {kw.title()}' section.",
                        suggestion=f"Add a '## {kw.title()}' section with concrete content.",
                    )
                )

        for kw in optional:
            if not self._has_section(headings, kw):
                issues.append(
                    Issue(
                        rule_id=self.id,
                        severity=self.severity,
                        line=None,
                        text=f"Missing optional section: {kw}",
                        explanation=f"README does not include a '## {kw.title()}' section.",
                        suggestion=f"Consider adding '## {kw.title()}' to set expectations and help contributors.",
                    )
                )

        # API Reference is conditional: required if README indicates it is a library.
        # Heuristic: contains 'pip install' or 'import ' and mentions 'library' or 'package'
        lowered = content.lower()
        looks_like_library = any(x in lowered for x in ["import ", "from "]) and any(
            x in lowered for x in ["library", "package", "python"]
        )
        if looks_like_library and not self._has_section(headings, "api") and not self._has_section(headings, "reference"):
            issues.append(
                Issue(
                    rule_id=self.id,
                    severity=self.severity,
                    line=None,
                    text="Missing section: API reference",
                    explanation="README appears to describe a library, but has no API reference section.",
                    suggestion="Add '## API Reference' with key functions, classes, and minimal examples.",
                )
            )

        return issues
