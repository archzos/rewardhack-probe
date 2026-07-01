# rewardhack-probe

[![CI](https://github.com/archzos/rewardhack-probe/actions/workflows/ci.yml/badge.svg)](https://github.com/archzos/rewardhack-probe/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

`rewardhack-probe` is a research-grade OSS probe harness for reward hacking
and emergent misalignment.

It has two jobs:

1. show reward hacking in small, auditable toy environments;
2. run an inference-time probe battery that looks for reward-hacking-adjacent
   behaviors in LLM outputs without training access.

This is a diagnostic instrument and demo suite, not a benchmark and not a
claim of production safety.

## What it provides

- A minimal gridworld with a deliberate specification gap
- A text game with an unstated-intent / stated-metric mismatch
- Probe batteries for sycophancy, specification gaming, eval awareness,
  goal substitution, and deceptive alignment signals
- DuckDB-backed report storage
- Streamlit dashboard for per-model and per-probe summaries
- CLI for toy-env demos, probe execution, and dashboards

## Open-source boundaries

- This repo is standalone research tooling.
- It does not depend on archzOS production systems.
- It is not affiliated with Anthropic, Redwood, OpenAI, or METR.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quick start

Run tests:

```bash
pytest
```

Run the gridworld demo:

```bash
rewardhack-probe toy-env --env gridworld --runs 3 --output-db report/results.duckdb --dry-run
```

Run a probe batch:

```bash
rewardhack-probe probe --categories sycophancy,spec_gaming --model mock:test --instances 20 --output-db report/results.duckdb --dry-run
```

## References

- Anthropic et al., *Natural Emergent Misalignment from Reward Hacking in Production RL* (arXiv:2511.18397)
- Denison et al., *Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models* (arXiv:2406.10162)
- OpenAI, *Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Deception*
- METR, *Recent Frontier Models Are Reward Hacking*

## Status

Day-1 scaffold: taxonomy, toy environments, probe battery skeleton, DuckDB
storage, dashboard, CLI, and tests.
