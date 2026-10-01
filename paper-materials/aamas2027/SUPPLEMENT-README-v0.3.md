# AAMAS 2027 supplementary material (anonymous staging package, v0.3)

This package contains the protocols, offline analysis scripts, sanitized run
summaries and trajectory records supporting the manuscript. It excludes raw
request directories, private credentials, account identifiers and local
filesystem paths. Public JSON artifacts recursively omit provider request IDs,
logical request IDs and system fingerprints.

The primary registered X2 estimand is the round-11 responder action. The
rounds 12--29 delayed-response file is a separate descriptive local-persistence
analysis; it is not a T4 test. P0-derived files and initial-state baselines are
offline sensitivity analyses and do not replace registered estimands.

## Current package contents

- Candidate A and four-arm ledgers, frozen analyses and sanitized metadata;
- exact observability and settlement certificates;
- prompt-difference, leading-indicator and structural sign-robustness analyses;
- Q-learning baseline, figure builders, protocols and provenance reports;
- public controlled-initial summaries and figures.

## Re-run examples

From the package root (Python 3.10+; `matplotlib` only for the figure):

```text
python tools/observability_certificate.py --check
python tools/candidate_a_structural.py --check
python tools/four_arm_leading_indicator.py --check
python tools/settlement_generalization.py --check
python tools/qlearning_baseline.py --render-only
python tools/build_fig2_replication.py
python tools/build_fig3_direction.py
python research/x1_best_response_probe.py --offline-selftest
python research/x2_forced_deviation.py --selftest
python research/qualify_x1_x2_statistics.py
python tools/verify_supplement.py aamas2027-supplement-v0.3.zip
```

The live runners are included for provenance but require an explicitly
configured environment and must not be run from this package during review.
Some research scripts refer to sealed author-side directories that are not
redistributed. All claims remain conditional on the tested DeepSeek
deployment, settlement rule and price grid; the package does not claim
collusion, a punishment equilibrium or a general false-negative rate.
