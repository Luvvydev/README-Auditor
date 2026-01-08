from __future__ import annotations

from readme_auditor.config import config_as_dict, load_config


def test_config_as_dict_returns_mapping():
    cfg = load_config(None)
    d = config_as_dict(cfg)
    assert isinstance(d, dict)
    assert "severity_threshold" in d
