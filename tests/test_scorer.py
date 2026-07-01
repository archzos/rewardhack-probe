"""Tests for probe scoring and confidence intervals."""

from rewardhack_probe.models import ProbeResult
from rewardhack_probe.scorer import score_category, score_report


def test_score_category_severity() -> None:
    results = [
        ProbeResult("sycophancy", "p", "r", True, 0.9, "e", "r"),
        ProbeResult("sycophancy", "p", "r", False, 0.1, "e", "r"),
    ]
    verdict = score_category("sycophancy", results)
    assert verdict.category == "sycophancy"
    assert verdict.detection_rate == 0.5
    assert verdict.severity == "HACKING_DETECTED"


def test_score_report_builds_category_breakdown() -> None:
    report = score_report(
        run_id="run-1",
        model_name="mock:test",
        run_type="probe",
        results_by_category={
            "sycophancy": [ProbeResult("sycophancy", "p", "r", True, 0.9, "e", "r")],
            "spec_gaming": [ProbeResult("spec_gaming", "p", "r", False, 0.1, "e", "r")],
        },
    )
    assert report.run_id == "run-1"
    assert len(report.category_results) == 2
