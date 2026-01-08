from __future__ import annotations

import json
from typing import Any, Dict

from ..models import AuditReport


class JsonFormatter:
    def render(self, report: AuditReport) -> str:
        return json.dumps(report.as_json_dict(), indent=2, sort_keys=False)

    def print(self, report: AuditReport) -> None:
        print(self.render(report))
