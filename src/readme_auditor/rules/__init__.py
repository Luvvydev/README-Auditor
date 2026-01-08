from __future__ import annotations

from typing import Dict, Type

from .assumed_knowledge import AssumedPriorKnowledgeRule
from .base import Rule
from .link_only_setup import LinkOnlySetupRule
from .missing_limitations import MissingLimitationsRule
from .missing_sections import MissingRequiredSectionsRule
from .no_examples import NoExamplesRule
from .no_troubleshooting import NoTroubleshootingRule
from .overpromising import OverpromisingScopeRule
from .unclear_audience import UnclearAudienceRule
from .unfalsifiable import UnfalsifiableClaimsRule
from .vague_claims import VagueClaimsRule

RULES: Dict[str, Type[Rule]] = {
    "vague_claims": VagueClaimsRule,
    "missing_sections": MissingRequiredSectionsRule,
    "unfalsifiable": UnfalsifiableClaimsRule,
    "link_only_setup": LinkOnlySetupRule,
    "assumed_knowledge": AssumedPriorKnowledgeRule,
    "no_examples": NoExamplesRule,
    "overpromising": OverpromisingScopeRule,
    "unclear_audience": UnclearAudienceRule,
    "no_troubleshooting": NoTroubleshootingRule,
    "missing_limitations": MissingLimitationsRule,
}


def list_rules() -> Dict[str, Type[Rule]]:
    return dict(RULES)
