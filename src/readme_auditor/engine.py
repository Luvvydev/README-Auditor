from __future__ import annotations

import datetime as _dt
from dataclasses import replace
from typing import Dict, Iterable, List, Optional, Tuple

from .models import AuditReport, AuditSummary, Config, Issue, Severity
from .parser import parse_markdown
from .rules import list_rules
from .rules.base import Rule


_SEV_ORDER: Dict[Severity, int] = {"info": 0, "warning": 1, "error": 2}


def severity_at_least(a: Severity, b: Severity) -> bool:
    return _SEV_ORDER[a] >= _SEV_ORDER[b]


def summarize(issues: List[Issue]) -> AuditSummary:
    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")
    info = sum(1 for i in issues if i.severity == "info")
    return AuditSummary(total=len(issues), errors=errors, warnings=warnings, info=info)


class AuditEngine:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._rule_types = list_rules()

    def available_rules(self) -> List[Tuple[str, str, str]]:
        out: List[Tuple[str, str, str]] = []
        for rid, cls in sorted(self._rule_types.items()):
            meta = cls.meta
            out.append((meta.rule_id, meta.name, meta.severity))
        return out

    def _instantiate_rules(self) -> List[Rule]:
        rules: List[Rule] = []
        for rid, cls in sorted(self._rule_types.items()):
            rc = self.cfg.rules.get(rid)
            if rc and not rc.enabled:
                continue
            severity_override = rc.severity if (rc and rc.severity) else None
            options = rc.options if rc else {}
            rules.append(cls(severity_override=severity_override, options=options))
        return rules

    def audit_content(self, *, filename: str, content: str) -> AuditReport:
        context = parse_markdown(content)
        issues: List[Issue] = []
        for rule in self._instantiate_rules():
            try:
                found = rule.check(content, context)
            except Exception as e:  # pragma: no cover
                # Defensive: rule bugs should not crash CI
                found = [
                    Issue(
                        rule_id=rule.id,
                        severity="error",
                        line=None,
                        text=f"Rule crashed: {rule.id}",
                        explanation=f"Exception: {type(e).__name__}: {e}",
                        suggestion="Fix the rule implementation or disable it in config.",
                        filename=filename,
                    )
                ]
            for iss in found:
                issues.append(replace(iss, filename=filename))

            # apply max issues early for performance
            if len(issues) >= self.cfg.max_issues:
                issues = issues[: self.cfg.max_issues]
                break

        # Apply severity threshold filter
        issues = [i for i in issues if severity_at_least(i.severity, self.cfg.severity_threshold)]
        summary = summarize(issues)
        passed = not any(severity_at_least(i.severity, self.cfg.fail_on) for i in issues)
        ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        return AuditReport(filename=filename, timestamp_utc=ts, issues=issues, summary=summary, passed=passed)
