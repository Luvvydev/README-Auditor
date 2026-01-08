from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from readme_auditor.cli import app
from readme_auditor.config import _parse_severity
from readme_auditor.formatters.human import HumanFormatter
from readme_auditor.models import AuditReport, AuditSummary, Issue


runner = CliRunner()


def test_cli_collect_targets_exists_but_not_file(tmp_path: Path):
    """
    Covers cli.py line 73 by forcing:
      p.exists() == True
      p.is_file() == False
    while still allowing directory scanning to succeed.
    """
    d = tmp_path / "proj"
    d.mkdir()

    # README.md exists but is a directory (not a file)
    (d / "README.md").mkdir()

    # Provide an actual markdown file so directory scanning succeeds
    (d / "doc.md").write_text(
        "# T\n\n## Installation\n\n```bash\nx\n```\n\n## Usage\n\n```bash\nx\n```\n\n## License\n\nMIT\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, [str(d)])
    assert result.exit_code == 0


def test_parse_severity_invalid_direct_call():
    """
    Covers config.py line 30 by directly exercising the invalid severity branch.
    """
    with pytest.raises(ValueError):
        _parse_severity("fatal", field_name="test")


def test_human_formatter_icon_fallback_used():
    """
    Covers human.py line 33 by forcing _icon() fallback during render().
    """
    report = AuditReport(
        filename="README.md",
        timestamp_utc="2026-01-07T00:00:00Z",
        issues=[
            Issue(
                rule_id="x",
                severity="weird",  # not in the map, forces "•"
                line=None,
                text="x",
                explanation="x",
                suggestion="",
            )
        ],
        summary=AuditSummary(total=1, errors=0, warnings=0, info=0),
        passed=True,
    )

    out = HumanFormatter(color=False).render(report)
    assert "•" in out
