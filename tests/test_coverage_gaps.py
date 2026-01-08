from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from readme_auditor.cli import app
from readme_auditor.config import load_config
from readme_auditor.formatters.human import _icon


runner = CliRunner()


def test_cli_collect_targets_returns_readme_variants(tmp_path: Path):
    d = tmp_path / "proj"
    d.mkdir()
    (d / "readme.md").write_text(
        "# T\n\n"
        "## Installation\n\n```bash\nx\n```\n\n"
        "## Usage\n\n```bash\nx\n```\n\n"
        "## License\n\nMIT\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, [str(d)])
    assert result.exit_code == 0


def test_cli_collect_targets_hits_readme_md_variant(tmp_path: Path):
    # This is intended to hit the README filename-variant branch in cli.py (line 73 in your report)
    d = tmp_path / "proj_variant"
    d.mkdir()
    (d / "Readme.md").write_text(
        "# T\n\n"
        "## Installation\n\n```bash\nx\n```\n\n"
        "## Usage\n\n```bash\nx\n```\n\n"
        "## License\n\nMIT\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, [str(d)])
    assert result.exit_code == 0


def test_cli_collect_targets_empty_dir_errors(tmp_path: Path):
    d = tmp_path / "empty"
    d.mkdir()

    result = runner.invoke(app, [str(d)])
    assert result.exit_code != 0
    assert "No README or markdown files found" in (result.stderr or result.output)


def test_load_config_invalid_general_severity_raises(tmp_path: Path):
    # This should hit config.py _parse_severity invalid branch (line 30 in your report)
    toml = tmp_path / "auditor.toml"
    toml.write_text(
        """
[general]
severity_threshold = "fatal"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_config(str(toml))


def test_load_config_invalid_rule_severity_raises(tmp_path: Path):
    toml = tmp_path / "auditor.toml"
    toml.write_text(
        """
[rules.vague_claims]
enabled = true
severity = "fatal"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_config(str(toml))


def test_load_config_invalid_output_format_raises(tmp_path: Path):
    toml = tmp_path / "auditor.toml"
    toml.write_text(
        """
[output]
format = "xml"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_config(str(toml))


def test_icon_fallback_branch():
    # This should hit human.py fallback branch (line 33 in your report)
    assert _icon("weird") == "•"
