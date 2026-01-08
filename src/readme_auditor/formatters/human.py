from __future__ import annotations

import io
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..models import AuditReport


def _icon(sev: str) -> str:
    return {"error": "❌", "warning": "⚠️ ", "info": "💡"}.get(sev, "•")


class HumanFormatter:
    def __init__(self, *, color: bool = True, show_suggestions: bool = True):
        self.console = Console(color_system="auto" if color else None, force_terminal=color)
        self.show_suggestions = show_suggestions

    def render(self, report: AuditReport) -> str:
        # Render to an in-memory console to avoid double-printing.
        buf = io.StringIO()
        con = Console(record=True, file=buf, color_system="auto")

        con.print(f"📄 {report.filename} - Found {report.summary.total} issues")

        for issue in report.issues:
            title = f"{_icon(issue.severity)} {issue.severity.upper()}: {issue.rule_id}"
            body_lines: List[str] = []
            if issue.line is not None:
                body_lines.append(f"Line {issue.line}: {issue.text}")
            else:
                body_lines.append(issue.text)
            body_lines.append(f"Why: {issue.explanation}")
            if self.show_suggestions and issue.suggestion:
                body_lines.append(f"Suggestion: {issue.suggestion}")
            con.print(Panel("\n".join(body_lines), title=title, expand=False))

        s = report.summary
        con.print(f"Summary: {s.errors} error, {s.warnings} warning, {s.info} info")
        return con.export_text()

    def print(self, report: AuditReport) -> None:
        text = self.render(report)
        self.console.print(Text.from_ansi(text))
