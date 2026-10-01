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

## Structural descriptive contrasts

Natural minus hide-rival equal-price persistence was 0.0000 in LL, LH and HH
complete-pair summaries, and 0.4213 in HL. These are descriptive arm-level
summaries from the incomplete run; they do not replace the registered
block-level estimands and are not evidence of collusion or strategic intent.

## Interpretation gate

Candidate A does not independently confirm a positive general tie effect. It
does provide a bounded replication in which the registered welfare contrasts
are near zero on complete blocks, while the $J$ completion range remains wide
enough to prevent a definitive equivalence claim. Candidate B should proceed
only as the separately registered feedback-surface mechanism experiment; it
must not be pooled with A or used to rescue a positive A result.
