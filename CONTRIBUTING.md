# Contributing to rewardhack-probe

This project focuses on auditable reward-hacking demos and inference-time
probe batteries, so changes should prioritize correctness and reproducibility.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Contribution workflow

1. Branch from `main`.
2. Keep changes scoped and test-backed.
3. Add or update tests for behavior changes.
4. Run `pytest` locally before opening a PR.
5. Call out any safety, evaluation, or API usage implications.

## Pull request checklist

- [ ] Tests added or updated
- [ ] Reproducibility considered
- [ ] README updated if user-facing behavior changed
- [ ] No secrets or credentials introduced

## Code style guidance

- Prefer explicit, deterministic logic.
- Keep toy environments short and auditable.
- Make probe scoring explainable.
