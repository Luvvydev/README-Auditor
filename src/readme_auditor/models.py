from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

Severity = Literal["info", "warning", "error"]


@dataclass(frozen=True)
class Issue:
    rule_id: str
    severity: Severity
    line: Optional[int]
    text: str
    explanation: str
    suggestion: str
    filename: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RuleMeta:
    rule_id: str
    name: str
    severity: Severity
    description: str


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    issues: List[Issue]


@dataclass(frozen=True)
class AuditSummary:
    total: int
    errors: int
    warnings: int
    info: int

    def as_dict(self) -> Dict[str, int]:
        return {"total": self.total, "errors": self.errors, "warnings": self.warnings, "info": self.info}


@dataclass(frozen=True)
class AuditReport:
    filename: str
    timestamp_utc: str
    issues: List[Issue]
    summary: AuditSummary
    passed: bool

    def as_json_dict(self) -> Dict[str, object]:
        return {
            "filename": self.filename,
            "timestamp": self.timestamp_utc,
            "issues": [
                {
                    "rule_id": i.rule_id,
                    "severity": i.severity,
                    "line": i.line,
                    "text": i.text,
                    "explanation": i.explanation,
                    "suggestion": i.suggestion,
                }
                for i in self.issues
            ],
            "summary": self.summary.as_dict(),
            "passed": self.passed,
        }


@dataclass
class RuleConfig:
    enabled: bool = True
    severity: Optional[Severity] = None
    options: Dict[str, object] = field(default_factory=dict)


@dataclass
class Config:
    severity_threshold: Severity = "warning"
    max_issues: int = 50
    output_format: Literal["human", "json"] = "human"
    color: bool = True
    show_suggestions: bool = True
    fail_on: Severity = "error"
    rules: Dict[str, RuleConfig] = field(default_factory=dict)
