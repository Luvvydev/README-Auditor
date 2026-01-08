from __future__ import annotations

from pathlib import Path

import pytest

from readme_auditor.config import load_config
from readme_auditor.models import Config


def test_load_config_defaults_when_none():
    cfg = load_config(None)
    assert isinstance(cfg, Config)
    assert cfg.severity_threshold in ("info", "warning", "error")


def test_load_config_from_toml(tmp_path: Path):
    toml = tmp_path / "auditor.toml"
    toml.write_text(
        """[general]
severity_threshold = "info"
max_issues = 10
fail_on = "warning"

[rules.vague_claims]
enabled = true
severity = "error"
custom_adjectives = ["blazing"]

[output]
format = "json"
color = false
show_suggestions = false
""",
        encoding="utf-8",
    )

    cfg = load_config(str(toml))
    assert cfg.severity_threshold == "info"
    assert cfg.max_issues == 10
    assert cfg.fail_on == "warning"
    assert cfg.output_format == "json"
    assert cfg.color is False
    assert cfg.show_suggestions is False

    rc = cfg.rules["vague_claims"]
    assert rc.enabled is True
    assert rc.severity == "error"
    assert rc.options["custom_adjectives"] == ["blazing"]


def test_load_config_invalid_severity_raises(tmp_path: Path):
    toml = tmp_path / "auditor.toml"
    toml.write_text(
        """[general]
severity_threshold = "fatal"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_config(str(toml))
