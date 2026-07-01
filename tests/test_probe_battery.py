"""Tests for the probe battery modules."""

from rewardhack_probe.cli import _MockAdapter
from rewardhack_probe.probe_battery import deceptive_alignment, eval_awareness, goal_substitution, spec_gaming, sycophancy


def test_probe_modules_return_results() -> None:
    adapter = _MockAdapter("mock:test")
    modules = [sycophancy, spec_gaming, eval_awareness, goal_substitution, deceptive_alignment]
    for module in modules:
        results = module.run_probe(adapter, {})
        assert results
        verdict = module.score_results(results)
        assert verdict.category == module.PROBE_CATEGORY


def test_sycophancy_detects_pressure_reversal() -> None:
    adapter = _MockAdapter("mock:test")
    results = sycophancy.run_probe(adapter, {})
    assert any(result.detected for result in results)
