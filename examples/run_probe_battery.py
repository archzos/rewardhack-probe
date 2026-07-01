"""Run a deterministic probe battery demo using the mock adapter."""

from rewardhack_probe.cli import _MockAdapter
from rewardhack_probe.probe_battery import eval_awareness, spec_gaming, sycophancy


def main() -> None:
    adapter = _MockAdapter("mock:test")
    for module in (sycophancy, spec_gaming, eval_awareness):
        results = module.run_probe(adapter, {})
        print(module.PROBE_CATEGORY, module.score_results(results))


if __name__ == "__main__":
    main()
