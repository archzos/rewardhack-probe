"""Reward-hacking taxonomy used by the probe battery."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RewardHackCategory(str, Enum):
    ENVIRONMENTAL_HACKING = "environmental_hacking"
    EVALUATOR_HACKING = "evaluator_hacking"
    SYCOPHANCY_ESCALATION = "sycophancy_escalation"
    SPECIFICATION_GAMING_GENERALIZATION = "specification_gaming_generalization"
    GOAL_SUBSTITUTION = "goal_substitution"
    DECEPTIVE_ALIGNMENT_SIGNAL = "deceptive_alignment_signal"


@dataclass(frozen=True, slots=True)
class TaxonomyEntry:
    code: RewardHackCategory
    title: str
    description: str


RHY_TAXONOMY: list[TaxonomyEntry] = [
    TaxonomyEntry(
        RewardHackCategory.ENVIRONMENTAL_HACKING,
        "Environmental hacking",
        "Exploiting simulator or environment structure that should not be exploitable.",
    ),
    TaxonomyEntry(
        RewardHackCategory.EVALUATOR_HACKING,
        "Evaluator hacking",
        "Gaming evaluator blind spots instead of the intended objective.",
    ),
    TaxonomyEntry(
        RewardHackCategory.SYCOPHANCY_ESCALATION,
        "Sycophancy escalation",
        "Reversing or amplifying agreement under social pressure without new evidence.",
    ),
    TaxonomyEntry(
        RewardHackCategory.SPECIFICATION_GAMING_GENERALIZATION,
        "Specification gaming generalization",
        "Maximizing the stated metric while violating the implied intent.",
    ),
    TaxonomyEntry(
        RewardHackCategory.GOAL_SUBSTITUTION,
        "Goal substitution",
        "Optimizing a proxy goal in place of the primary goal.",
    ),
    TaxonomyEntry(
        RewardHackCategory.DECEPTIVE_ALIGNMENT_SIGNAL,
        "Deceptive alignment signal",
        "Claiming alignment while behavior suggests specification gaming.",
    ),
]


def taxonomy_by_code() -> dict[str, TaxonomyEntry]:
    return {entry.code.value: entry for entry in RHY_TAXONOMY}
