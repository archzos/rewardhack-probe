# Reward Hacking Taxonomy

This repository uses the following probe categories as its labeled source of
truth:

- `environmental_hacking`
- `evaluator_hacking`
- `sycophancy_escalation`
- `specification_gaming_generalization`
- `goal_substitution`
- `deceptive_alignment_signal`

These map to probe modules in `rewardhack_probe/probe_battery/`.

## Operational meanings

- `environmental_hacking`: exploiting the environment or simulator structure.
- `evaluator_hacking`: gaming the evaluator's blind spots rather than the
  intended objective.
- `sycophancy_escalation`: reversing or amplifying agreement under pressure
  without new evidence.
- `specification_gaming_generalization`: maximizing the stated metric while
  violating the implied intent.
- `goal_substitution`: optimizing a proxy goal in place of the primary goal.
- `deceptive_alignment_signal`: claiming alignment while the behavioral trace
  suggests otherwise.

## Notes

The probes in this repo are inference-time operationalizations. They are not a
claim to reproduce training-time emergent misalignment.
