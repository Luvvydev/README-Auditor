from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from readme_auditor.cli import app
from readme_auditor.config import load_config
from readme_auditor.formatters.human import HumanFormatter
from readme_auditor.models import AuditReport, AuditSummary, Issue


runner = CliRunner()


def test_cli_target_does_not_exist_hits_badparameter(tmp_path: Path):
    # Covers src/readme_auditor/cli.py line 73:
    #   if not target.exists(): raise typer.BadParameter(...)
    missing = tmp_path / "does-not-exist"

    result = runner.invoke(app, [str(missing)])
    assert result.exit_code != 0
    assert "Target does not exist" in (result.stderr or result.output)


def test_load_config_missing_file_raises(tmp_path: Path):
    # Covers src/readme_auditor/config.py line 30:
    #   if not os.path.exists(path): raise FileNotFoundError(...)
    missing = tmp_path / "nope.toml"
    with pytest.raises(FileNotFoundError):
        load_config(str(missing))


def test_human_formatter_line_not_none_branch():
    # Covers src/readme_auditor/formatters/human.py line 33:
    #   if issue.line is not None: body_lines.append(f"Line {issue.line}: ...")
    report = AuditReport(
        filename="README.md",
        timestamp_utc="2026-01-07T00:00:00Z",
        issues=[
            Issue(
                rule_id="x",
                severity="warning",
                line=12,  # triggers the branch
                text="example line text",
                explanation="example explanation",
                suggestion="",
            )
        ],
        summary=AuditSummary(total=1, errors=0, warnings=1, info=0),
        passed=False,
    )

    out = HumanFormatter(color=False).render(report)
    assert "Line 12:" in out
