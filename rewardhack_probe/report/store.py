"""DuckDB persistence for reward-hack probe runs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import duckdb

from rewardhack_probe.models import EnvHackResult, ProbeResult, RewardHackReport


def initialize_db(db_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                run_type TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                metadata_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS category_results (
                run_id TEXT NOT NULL,
                category TEXT NOT NULL,
                detection_rate DOUBLE NOT NULL,
                confidence_low DOUBLE NOT NULL,
                confidence_high DOUBLE NOT NULL,
                severity TEXT NOT NULL,
                sample_size INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS probe_results (
                run_id TEXT NOT NULL,
                category TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                detected BOOLEAN NOT NULL,
                confidence DOUBLE NOT NULL,
                evidence_excerpt TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS env_results (
                run_id TEXT NOT NULL,
                env_name TEXT NOT NULL,
                episode_id TEXT NOT NULL,
                actual_success BOOLEAN NOT NULL,
                claimed_success BOOLEAN NOT NULL,
                reward DOUBLE NOT NULL,
                hack_detected BOOLEAN NOT NULL,
                evidence_excerpt TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            )
            """
        )


def write_report(*, db_path: str, report: RewardHackReport, probe_results: dict[str, list[ProbeResult]] | None = None, env_results: list[EnvHackResult] | None = None) -> None:
    initialize_db(db_path)
    with duckdb.connect(db_path) as conn:
        conn.execute("DELETE FROM runs WHERE run_id = ?", [report.run_id])
        conn.execute("DELETE FROM category_results WHERE run_id = ?", [report.run_id])
        conn.execute("DELETE FROM probe_results WHERE run_id = ?", [report.run_id])
        conn.execute("DELETE FROM env_results WHERE run_id = ?", [report.run_id])
        conn.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?)",
            [report.run_id, report.model_name, report.run_type, datetime.now(UTC).replace(tzinfo=None), json.dumps(report.metadata)],
        )
        conn.executemany(
            "INSERT INTO category_results VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                [
                    report.run_id,
                    row["category"],
                    row["detection_rate"],
                    row["confidence_low"],
                    row["confidence_high"],
                    row["severity"],
                    row["sample_size"],
                ]
                for row in report.category_results
            ],
        )
        if probe_results:
            probe_rows = []
            for category, results in probe_results.items():
                for result in results:
                    probe_rows.append(
                        [
                            report.run_id,
                            category,
                            result.prompt,
                            result.response,
                            result.detected,
                            result.confidence,
                            result.evidence_excerpt,
                            result.reasoning,
                            json.dumps(result.metadata),
                        ]
                    )
            if probe_rows:
                conn.executemany("INSERT INTO probe_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", probe_rows)
        if env_results:
            env_rows = [
                [
                    report.run_id,
                    row.env_name,
                    row.episode_id,
                    row.actual_success,
                    row.claimed_success,
                    row.reward,
                    row.hack_detected,
                    row.evidence_excerpt,
                    json.dumps(row.metadata),
                ]
                for row in env_results
            ]
            conn.executemany("INSERT INTO env_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", env_rows)


def fetch_latest_report(db_path: str) -> dict[str, object] | None:
    initialize_db(db_path)
    with duckdb.connect(db_path) as conn:
        run = conn.execute(
            """
            SELECT run_id, model_name, run_type, metadata_json
            FROM runs
            ORDER BY created_at DESC
            LIMIT 1
            """
        ).fetchone()
        if run is None:
            return None
        categories = conn.execute(
            """
            SELECT category, detection_rate, confidence_low, confidence_high, severity, sample_size
            FROM category_results
            WHERE run_id = ?
            ORDER BY category
            """,
            [run[0]],
        ).fetchall()
    return {
        "run_id": run[0],
        "model_name": run[1],
        "run_type": run[2],
        "metadata": json.loads(run[3]),
        "category_results": [
            {
                "category": row[0],
                "detection_rate": row[1],
                "confidence_low": row[2],
                "confidence_high": row[3],
                "severity": row[4],
                "sample_size": row[5],
            }
            for row in categories
        ],
    }


def fetch_dashboard_payload(db_path: str) -> dict[str, object]:
    initialize_db(db_path)
    with duckdb.connect(db_path) as conn:
        latest = fetch_latest_report(db_path)
        model_counts = conn.execute(
            """
            SELECT model_name, COUNT(*)
            FROM runs
            GROUP BY model_name
            ORDER BY COUNT(*) DESC, model_name
            """
        ).fetchall()
        category_counts = conn.execute(
            """
            SELECT category, AVG(detection_rate), AVG(confidence_low), AVG(confidence_high)
            FROM category_results
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()
        probe_rows = conn.execute(
            """
            SELECT category, detected, confidence
            FROM probe_results
            """
        ).fetchall()
    return {
        "latest": latest,
        "model_counts": [{"model_name": row[0], "count": row[1]} for row in model_counts],
        "category_aggregates": [
            {"category": row[0], "avg_detection_rate": row[1], "avg_confidence_low": row[2], "avg_confidence_high": row[3]}
            for row in category_counts
        ],
        "probe_rows": [
            {"category": row[0], "detected": row[1], "confidence": row[2]}
            for row in probe_rows
        ],
    }
