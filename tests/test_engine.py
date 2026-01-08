from __future__ import annotations

from readme_auditor.engine import AuditEngine
from readme_auditor.models import Config


def test_engine_filters_by_threshold():
    cfg = Config()
    cfg.severity_threshold = "error"
    engine = AuditEngine(cfg)

    content = "# X\n\n## Usage\n\nNo code\n\n## Installation\n\nRun it\n\n## License\n\nMIT\n"
    report = engine.audit_content(filename="README.md", content=content)
    # Only errors at threshold
    assert all(i.severity == "error" for i in report.issues)
