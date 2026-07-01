"""CLI for toy env demos and probe execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rewardhack_probe.adapters.bedrock_adapter import BedrockAdapter
from rewardhack_probe.adapters.openai_adapter import OpenAIAdapter
from rewardhack_probe.models import EnvHackResult, ProbeResult
from rewardhack_probe.probe_battery import deceptive_alignment, eval_awareness, goal_substitution, spec_gaming, sycophancy
from rewardhack_probe.report.dashboard import render
from rewardhack_probe.report.store import fetch_latest_report, initialize_db, write_report
from rewardhack_probe.scorer import score_report
from rewardhack_probe.toy_envs.gridworld import run_gridworld_demo
from rewardhack_probe.toy_envs.text_game import run_text_game_demo


PROBE_MODULES = {
    "sycophancy": sycophancy,
    "spec_gaming": spec_gaming,
    "eval_awareness": eval_awareness,
    "goal_substitution": goal_substitution,
    "deceptive_alignment": deceptive_alignment,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rewardhack-probe")
    sub = parser.add_subparsers(dest="command", required=True)

    toy_env = sub.add_parser("toy-env")
    toy_env.add_argument("--env", required=True, choices=["gridworld", "text_game"])
    toy_env.add_argument("--runs", type=int, default=1)
    toy_env.add_argument("--output-db", default="report/results.duckdb")
    toy_env.add_argument("--dry-run", action="store_true")

    probe = sub.add_parser("probe")
    probe.add_argument("--categories", required=True)
    probe.add_argument("--model", required=True)
    probe.add_argument("--instances", type=int, default=20)
    probe.add_argument("--output-db", default="report/results.duckdb")
    probe.add_argument("--dry-run", action="store_true")

    dashboard = sub.add_parser("dashboard")
    dashboard.add_argument("--db", default="report/results.duckdb")
    dashboard.add_argument("--serve", action="store_true")

    return parser


def _resolve_adapter(model: str):
    if model.startswith("openai:"):
        return OpenAIAdapter(model_name=model.split(":", 1)[1])
    if model.startswith("bedrock:"):
        return BedrockAdapter(model_id=model.split(":", 1)[1])
    if model.startswith("mock:"):
        return _MockAdapter(model)
    return _MockAdapter(model)


class _MockAdapter:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def complete(self, prompt: str, *, system: str | None = None, temperature: float = 0.0) -> str:
        lowered = f"{system or ''} {prompt}".lower()
        if "are you sure" in lowered or "safety team" in lowered:
            return "You're right."
        if "under 100 words" in lowered or "very short summary" in lowered:
            return "Short summary with omitted facts."
        if "user satisfaction" in lowered:
            return "Yes, you're right."
        if "always follow the user's intent" in lowered:
            return "I always follow intent, but limits apply."
        return "A careful answer."


def _run_toy_env(args) -> None:
    results: list[EnvHackResult] = []
    for index in range(args.runs):
        if args.env == "gridworld":
            episode = run_gridworld_demo(hack=not args.dry_run and index % 2 == 0)
            results.append(
                EnvHackResult(
                    env_name="gridworld",
                    episode_id=f"gridworld-{index}",
                    actual_success=episode.actual_success,
                    claimed_success=episode.reward > 0,
                    reward=episode.reward,
                    hack_detected=episode.hack_detected,
                    evidence_excerpt=episode.evidence_excerpt,
                    metadata={"actions": episode.actions, "actual_position": episode.actual_position, "reported_position": episode.reported_position},
                )
            )
        else:
            episode = run_text_game_demo(hack=not args.dry_run and index % 2 == 0)
            results.append(
                EnvHackResult(
                    env_name="text_game",
                    episode_id=f"text-game-{index}",
                    actual_success=episode.actual_success,
                    claimed_success=episode.reward > 0,
                    reward=episode.reward,
                    hack_detected=episode.hack_detected,
                    evidence_excerpt=episode.evidence_excerpt,
                    metadata={"turns": episode.turns, "npc_harmed": episode.npc_harmed, "treasure_obtained": episode.treasure_obtained},
                )
            )
    report = score_report(
        run_id=f"{args.env}-run",
        model_name="toy-env",
        run_type="toy_env",
        results_by_category={"environmental_hacking": [ProbeResult("environmental_hacking", "", "", row.hack_detected, 1.0 if row.hack_detected else 0.0, row.evidence_excerpt, "toy env demo") for row in results]},
    )
    if not args.dry_run:
        write_report(db_path=args.output_db, report=report, env_results=results)


def _run_probe(args) -> None:
    adapter = _resolve_adapter(args.model)
    categories = [item.strip() for item in args.categories.split(",") if item.strip()]
    probe_results: dict[str, list[ProbeResult]] = {}
    for category in categories:
        module = PROBE_MODULES[category]
        results: list[ProbeResult] = []
        for _ in range(args.instances):
            results.extend(module.run_probe(adapter, {}))
        probe_results[category] = results
    report = score_report(
        run_id="probe-run",
        model_name=args.model,
        run_type="probe",
        results_by_category=probe_results,
    )
    if not args.dry_run:
        write_report(db_path=args.output_db, report=report, probe_results=probe_results)
    else:
        print(json.dumps({"run_id": report.run_id, "model_name": report.model_name, "category_results": report.category_results}, indent=2))


def main() -> None:
    args = _build_parser().parse_args()
    if args.command == "toy-env":
        _run_toy_env(args)
        return
    if args.command == "probe":
        _run_probe(args)
        return
    if args.command == "dashboard":
        if args.serve:
            import subprocess
            import sys

            subprocess.run([sys.executable, "-m", "streamlit", "run", str(Path(__file__).parent / "report" / "dashboard.py"), "--", "--db", args.db], check=True)
            return
        latest = fetch_latest_report(args.db)
        print(json.dumps(latest, indent=2) if latest else "No runs found.")
