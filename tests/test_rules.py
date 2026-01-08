from __future__ import annotations

from readme_auditor.engine import AuditEngine
from readme_auditor.models import Config
from readme_auditor.parser import parse_markdown
from readme_auditor.rules.vague_claims import VagueClaimsRule
from readme_auditor.rules.missing_sections import MissingRequiredSectionsRule
from readme_auditor.rules.no_examples import NoExamplesRule
from readme_auditor.rules.unfalsifiable import UnfalsifiableClaimsRule
from readme_auditor.rules.overpromising import OverpromisingScopeRule


def test_vague_claims_triggers_without_evidence():
    content = "A fast and simple tool.\n"
    ctx = parse_markdown(content)
    rule = VagueClaimsRule()
    issues = rule.check(content, ctx)
    assert issues
    assert any("fast" in i.explanation.lower() or "simple" in i.explanation.lower() for i in issues)


def test_vague_claims_ignored_with_numbers():
    content = "A fast tool: 2x speedup on dataset X.\n"
    ctx = parse_markdown(content)
    rule = VagueClaimsRule()
    issues = rule.check(content, ctx)
    assert not issues


def test_missing_sections_errors_for_install_and_usage():
    content = "# Title\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    rule = MissingRequiredSectionsRule()
    issues = rule.check(content, ctx)
    severities = {i.severity for i in issues}
    assert "error" in severities


def test_no_examples_triggers_when_usage_has_no_code():
    content = "# Title\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\nRun it.\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    rule = NoExamplesRule()
    issues = rule.check(content, ctx)
    assert issues


def test_no_examples_passes_when_usage_has_code():
    content = "# Title\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    rule = NoExamplesRule()
    issues = rule.check(content, ctx)
    assert not issues


def test_unfalsifiable_triggers():
    content = "This never crashes.\n"
    ctx = parse_markdown(content)
    rule = UnfalsifiableClaimsRule()
    issues = rule.check(content, ctx)
    assert issues


def test_overpromising_triggers():
    content = "Everything you need for documentation.\n"
    ctx = parse_markdown(content)
    rule = OverpromisingScopeRule()
    issues = rule.check(content, ctx)
    assert issues
