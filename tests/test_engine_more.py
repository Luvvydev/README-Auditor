from __future__ import annotations

from readme_auditor.engine import AuditEngine
from readme_auditor.models import Config, RuleConfig


def test_engine_can_disable_rule_via_config():
    cfg = Config()
    cfg.rules["missing_limitations"] = RuleConfig(enabled=False)
    engine = AuditEngine(cfg)

    content = "# T\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Troubleshooting\n\nText\n\n## License\n\nMIT\n"
    report = engine.audit_content(filename="README.md", content=content)
    assert all(i.rule_id != "missing_limitations" for i in report.issues)


def test_engine_max_issues_limits_and_breaks():
    cfg = Config()
    cfg.max_issues = 1
    engine = AuditEngine(cfg)

    content = "# T\n\nA fast and simple tool.\n"
    report = engine.audit_content(filename="README.md", content=content)
    assert len(report.issues) == 1
