from __future__ import annotations

from readme_auditor.parser import parse_markdown
from readme_auditor.rules.missing_sections import MissingRequiredSectionsRule
from readme_auditor.rules.no_examples import NoExamplesRule
from readme_auditor.rules.overpromising import OverpromisingScopeRule
from readme_auditor.rules.unfalsifiable import UnfalsifiableClaimsRule
from readme_auditor.rules.vague_claims import VagueClaimsRule
from readme_auditor.rules.assumed_knowledge import AssumedPriorKnowledgeRule


def test_missing_sections_options_override_lists():
    content = "# T\n\n## Setup\n\nText\n"
    ctx = parse_markdown(content)
    rule = MissingRequiredSectionsRule(options={"required": ["setup"], "optional": ["changelog"]})
    issues = rule.check(content, ctx)
    # setup exists so it should not be flagged as missing, but changelog optional should be
    assert any("optional" in i.text.lower() for i in issues)


def test_no_examples_branch_when_no_usage_section():
    content = "# T\n\n## Installation\n\n```bash\npip install x\n```\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = NoExamplesRule().check(content, ctx)
    assert issues and issues[0].line is None


def test_overpromising_ignored_when_bounded():
    content = "Everything you need, limited to this project.\n"
    ctx = parse_markdown(content)
    issues = OverpromisingScopeRule().check(content, ctx)
    assert not issues


def test_unfalsifiable_ignored_with_caveat_word():
    content = "This always works for most cases.\n"
    ctx = parse_markdown(content)
    issues = UnfalsifiableClaimsRule().check(content, ctx)
    assert not issues


def test_vague_claims_custom_adjective_detected():
    content = "A blazing tool.\n"
    ctx = parse_markdown(content)
    rule = VagueClaimsRule(options={"custom_adjectives": ["blazing"]})
    issues = rule.check(content, ctx)
    assert issues


def test_vague_claims_evidence_on_next_line_suppresses():
    content = "A fast tool\n2x speedup on dataset X\n"
    ctx = parse_markdown(content)
    issues = VagueClaimsRule().check(content, ctx)
    assert not issues


def test_assumed_knowledge_ignored_when_requirements_present():
    content = "# T\n\n## Installation\n\nRequirements: make\nJust run make\n\n## Usage\n\n```bash\nx --help\n```\n\n## License\n\nMIT\n"
    ctx = parse_markdown(content)
    issues = AssumedPriorKnowledgeRule().check(content, ctx)
    assert not issues
