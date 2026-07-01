"""Streamlit dashboard for reward-hack probe reports."""

from __future__ import annotations

import argparse
from collections import Counter

import plotly.express as px
import streamlit as st

from rewardhack_probe.report.store import fetch_dashboard_payload


def render(db_path: str) -> None:
    st.set_page_config(page_title="rewardhack-probe", layout="wide")
    st.title("rewardhack-probe dashboard")

    payload = fetch_dashboard_payload(db_path)
    latest = payload["latest"]
    if latest is None:
        st.info("No runs found. Execute `rewardhack-probe probe` or `rewardhack-probe toy-env` first.")
        return

    st.subheader(f"Run {latest['run_id']} - {latest['model_name']}")
    st.caption(latest["run_type"])

    st.dataframe(latest["category_results"], use_container_width=True)

    columns = st.columns(2)
    with columns[0]:
        st.subheader("Model counts")
        st.dataframe(payload["model_counts"], use_container_width=True)
    with columns[1]:
        st.subheader("Category averages")
        st.dataframe(payload["category_aggregates"], use_container_width=True)

    if payload["probe_rows"]:
        counts = Counter((row["category"], bool(row["detected"])) for row in payload["probe_rows"])
        fig = px.bar(
            x=[f"{category}:{detected}" for category, detected in counts.keys()],
            y=list(counts.values()),
            labels={"x": "category / detected", "y": "count"},
            title="Probe detection counts",
        )
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="report/results.duckdb")
    args = parser.parse_args()
    render(args.db)


if __name__ == "__main__":
    main()
