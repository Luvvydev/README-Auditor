from __future__ import annotations

from readme_auditor.parser import parse_markdown
from readme_auditor.rules.base import Rule
from readme_auditor.models import Issue, RuleMeta
from readme_auditor.rules.link_only_setup import LinkOnlySetupRule
from readme_auditor.rules.assumed_knowledge import AssumedPriorKnowledgeRule
from readme_auditor.rules.no_troubleshooting import NoTroubleshootingRule
from readme_auditor.rules.missing_limitations import MissingLimitationsRule
from readme_auditor.rules.unclear_audience import UnclearAudienceRule


class _DummyRule(Rule):
    meta = RuleMeta(rule_id="dummy", name="Dummy", severity="info", description="dummy")
    def check(self, content: str, context: dict) -> list[Issue]:
        return []


def test_rule_base_properties_covered():
    r = _DummyRule()
    assert r.id == "dummy"
    assert r.name == "Dummy"
    assert r.description == "dummy"
    assert r.severity == "info"


def test_link_only_setup_triggers_when_no_code_blocks():
    content = "# T\n\n## Installation\n\nSee docs: https://example.com/docs\n\n## Usage\n\n```bash\nx --help\n```\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = LinkOnlySetupRule().check(content, ctx)
    assert issues
    assert issues[0].rule_id == "link_only_setup"


def test_assumed_knowledge_triggers_on_just_run_without_prereqs():
    content = "# T\n\n## Installation\n\nJust run make\n\n## Usage\n\n```bash\nx --help\n```\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = AssumedPriorKnowledgeRule().check(content, ctx)
    assert issues
    assert issues[0].severity == "info"


def test_no_troubleshooting_triggers_when_missing():
    content = "# T\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Limitations\n\nText\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = NoTroubleshootingRule().check(content, ctx)
    assert issues


def test_missing_limitations_passes_when_present():
    content = "# T\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Troubleshooting\n\nText\n\n## Limitations\n\nText\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = MissingLimitationsRule().check(content, ctx)
    assert not issues


def test_unclear_audience_triggers_when_no_keywords():
    content = "# Title\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Troubleshooting\n\nText\n\n## Limitations\n\nText\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = UnclearAudienceRule().check(content, ctx)
    assert issues
