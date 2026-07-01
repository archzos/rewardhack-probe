"""Tests for report persistence."""

from rewardhack_probe.cli import _MockAdapter
from rewardhack_probe.models import EnvHackResult
from rewardhack_probe.probe_battery import eval_awareness
from rewardhack_probe.report.store import fetch_dashboard_payload, fetch_latest_report, write_report
from rewardhack_probe.scorer import score_report


def test_write_and_fetch_report(tmp_path) -> None:
    adapter = _MockAdapter("mock:test")
    results = eval_awareness.run_probe(adapter, {})
    report = score_report(
        run_id="run-1",
        model_name="mock:test",
        run_type="probe",
        results_by_category={"eval_awareness": results},
    )
    db_path = tmp_path / "results.duckdb"
    write_report(db_path=str(db_path), report=report, probe_results={"eval_awareness": results})

    latest = fetch_latest_report(str(db_path))
    assert latest is not None
    assert latest["run_id"] == "run-1"

    payload = fetch_dashboard_payload(str(db_path))
    assert payload["latest"]["run_id"] == "run-1"


def test_env_result_persistence(tmp_path) -> None:
    report = score_report(
        run_id="grid-1",
        model_name="toy-env",
        run_type="toy_env",
        results_by_category={"environmental_hacking": []},
    )
    db_path = tmp_path / "results.duckdb"
    write_report(
        db_path=str(db_path),
        report=report,
        env_results=[
            EnvHackResult(
                env_name="gridworld",
                episode_id="ep-1",
                actual_success=False,
                claimed_success=True,
                reward=1.0,
                hack_detected=True,
                evidence_excerpt="reported goal without reaching goal",
            )
        ],
    )
    latest = fetch_latest_report(str(db_path))
    assert latest is not None
