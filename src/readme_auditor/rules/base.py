from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from ..models import Issue, RuleMeta, Severity


class Rule(ABC):
    """Abstract base class for all audit rules."""

    meta: RuleMeta

    def __init__(self, *, severity_override: Severity | None = None, options: Dict[str, object] | None = None):
        self._severity_override = severity_override
        self.options: Dict[str, object] = options or {}

    @property
    def id(self) -> str:
        return self.meta.rule_id

    @property
    def name(self) -> str:
        return self.meta.name

    @property
    def description(self) -> str:
        return self.meta.description

    @property
    def severity(self) -> Severity:
        return self._severity_override or self.meta.severity

    @abstractmethod
    def check(self, content: str, context: Dict[str, object]) -> List[Issue]:
        raise NotImplementedError  # pragma: no cover
