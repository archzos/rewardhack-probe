# ArchzOS Agent Architecture Context

`rewardhack-probe` is a standalone research tool for observing reward-hacking
behaviors in toy environments and LLM probe batteries.

## 1) Why this repo exists

The project exists to make reward hacking observable without needing access to
production training infrastructure.

## 2) Where it fits

- `trifecta-guard`: runtime security enforcement.
- `mast-doctor`: multi-agent failure diagnosis.
- `rewardhack-probe`: reward-hacking demos and probe battery.

## 3) Boundary

This repo does not depend on archzOS production systems. That boundary is
deliberate and should remain clear in code, docs, and releases.
