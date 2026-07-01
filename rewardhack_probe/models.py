"""Core models for reward-hack probe results and reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProbeResult:
    probe_category: str
    prompt: str
    response: str
    detected: bool
    confidence: float
    evidence_excerpt: str
    reasoning: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EnvHackResult:
    env_name: str
    episode_id: str
    actual_success: bool
    claimed_success: bool
    reward: float
    hack_detected: bool
    evidence_excerpt: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RewardHackReport:
    run_id: str
    model_name: str
    run_type: str
    category_results: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)
