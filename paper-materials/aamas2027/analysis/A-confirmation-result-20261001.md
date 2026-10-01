# Candidate A independent confirmation: result record

## Execution

- Parent attempt: 308 complete, 7 failed; stopped by a local Windows durable-
  ledger error while replacing a 21 MB `cells.json` file.
- Continuation: 68 remaining cells were executed from a new sealed snapshot
  with the ledger-replacement retry window amended. No prior model request was
  resumed or retried.
- Combined result: 376/384 trajectories complete and 8/384 failed (2.08%).
- Delivered requests: 21,998; accounted/reserved amount: 42.956636 CNY.
- Final state: `finished_with_missing`; no cells remain unstarted.

## Registered welfare contrasts

| estimand | complete blocks | mean | Bonferroni 95% interval | completion range |
|---|---:|---:|---:|---:|
| $D_{asym}$ | 42 | 0.2257 | [-0.2994, 0.7508] | [-3.1988, 4.8416] |
| $J$ | 40 | 0.2370 | [-0.3155, 0.7894] | [-4.8915, 5.6879] |

Both observed intervals are compatible with a practically small welfare
contrast. With the candidate $\delta_W=5$, the observed-complete intervals
fall inside the equivalence margin, but the missing-outcome completion range
for $J$ exceeds the upper margin. The confirmatory equivalence decision is
therefore **inconclusive under the registered missingness sensitivity**, not a
proof of equivalence.

## Structural primary (added 2026-10-01; corrects the earlier version)

> **Correction.** The first version of this record stated that "natural minus
> hide-rival equal-price persistence was 0.0000 in LL, LH and HH complete-pair
> summaries, and 0.4213 in HL" and concluded that Candidate A "does not
> independently confirm a positive general tie effect". Those four numbers are
> the `descriptive_deltas` field of `data/A-confirmation-analysis.json`, which
> are **hide-rival-minus-natural welfare** deltas, not equal-price persistence.
> The protocol's structural primary had not been computed. It is now computed
> from the sealed ledger by `tools/candidate_a_structural.py`, which also
> reproduces every number in the frozen analysis file exactly (the frozen file
> is not modified). Full tables: `A-confirmation-structural-20261001.md`.

Natural minus hide-rival equal-price fraction over assessment rounds 10--29,
aggregated within trajectory and paired by block:

| contrast | complete blocks | mean | block-t 95% interval | + / 0 / − blocks | completion range |
|---|---:|---:|---:|---|---:|
| LH | 45 | 0.819 | [0.712, 0.926] | 42 / 3 / 0 | — |
| HL | 45 | 0.842 | [0.739, 0.945] | 41 / 4 / 0 | — |
| $D_{\mathrm{tie}}$ | 42 | 0.830 | [0.743, 0.917] | 42 / 0 / 0 | [0.792, 0.841] |

The protocol's structural decision rule is met: the 95% interval for
$D_{\mathrm{tie}}$ excludes zero in the registered direction, and so does the
entire missing-outcome completion range. Round-1 tie counts reproduce the
original first-decision pattern (LH: 15/46 natural vs 0/47 hide-rival; HL:
29/47 vs 0/46), and neither hide-rival asymmetric cell reached a tie in any
assessment round.

The descriptive welfare deltas (hide-rival minus natural, complete pairs) are
0.0000 (LL), 0.0000 (LH), 0.4213 (HL) and 0.0000 (HH): in LH the structural
change occurs entirely inside the minimum-price-6.0 equivalence class.

## Interpretation gate (revised)

Candidate A confirms the structural (T2/T3) contrast within the same model
deployment: display policy changes equal-price persistence by about 0.83 of
the assessment window while the registered welfare contrasts stay near zero on
complete blocks. The welfare-equivalence decision remains inconclusive because
the registered full-support completion range for $J$ exceeds $\delta_W=5$.
This is a within-deployment replication (same alias and returned
fingerprint), not a cross-model test, and it is not evidence of collusion,
punishment or strategic intent. Candidate B should proceed only as the
separately registered feedback-surface mechanism experiment; it must not be
pooled with A.
