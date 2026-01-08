from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from .models import Config, RuleConfig, Severity

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


_SEVERITIES: tuple[Severity, ...] = ("info", "warning", "error")


def _parse_severity(value: str, *, field_name: str) -> Severity:
    v = value.strip().lower()
    if v not in _SEVERITIES:
        raise ValueError(f"Invalid {field_name}: {value!r}. Expected one of: {', '.join(_SEVERITIES)}")
    return v  # type: ignore[return-value]


def load_config(path: Optional[str]) -> Config:
    cfg = Config()
    if not path:
        return cfg
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    data = tomllib.loads(open(path, "rb").read().decode("utf-8"))

    general = data.get("general", {})
    if "severity_threshold" in general:
        cfg.severity_threshold = _parse_severity(general["severity_threshold"], field_name="severity_threshold")
    if "max_issues" in general:
        cfg.max_issues = int(general["max_issues"])

    output = data.get("output", {})
    if "format" in output:
        fmt = str(output["format"]).strip().lower()
        if fmt not in ("human", "json"):
            raise ValueError("output.format must be 'human' or 'json'")
        cfg.output_format = fmt  # type: ignore[assignment]
    if "color" in output:
        cfg.color = bool(output["color"])
    if "show_suggestions" in output:
        cfg.show_suggestions = bool(output["show_suggestions"])

    rules = data.get("rules", {})
    for rule_id, rule_data in rules.items():
        rc = RuleConfig()
        if isinstance(rule_data, dict):
            if "enabled" in rule_data:
                rc.enabled = bool(rule_data["enabled"])
            if "severity" in rule_data and rule_data["severity"] is not None:
                rc.severity = _parse_severity(str(rule_data["severity"]), field_name=f"rules.{rule_id}.severity")
            # everything else is options
            rc.options = {k: v for k, v in rule_data.items() if k not in {"enabled", "severity"}}
        cfg.rules[str(rule_id)] = rc

    if "fail_on" in data.get("general", {}):
        cfg.fail_on = _parse_severity(str(general["fail_on"]), field_name="fail_on")

    return cfg


def config_as_dict(cfg: Config) -> Dict[str, Any]:
    d = asdict(cfg)
    # dataclasses serialize RuleConfig objects already, fine for debugging
    return d
