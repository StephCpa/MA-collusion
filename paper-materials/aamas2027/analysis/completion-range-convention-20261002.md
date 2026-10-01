# Completion-range convention audit

This is an offline reconstruction of the missing-outcome support convention;
it is not evidence that the convention was pre-registered before the original
run.

The frozen Candidate A analysis and its reproduction code use the following
rule:

1. Keep every observed assessment-round welfare value, including values from a
   partial trajectory.
2. For each unresolved assessment round, allow the welfare to range over the
   full registered grid support, from welfare at price 6.5 (`281.9444`) to
   welfare at price 2.0 (`444.4444`).
3. Form the lower and upper trajectory means, then apply the signed contrast
   coefficients at the block level and average the resulting lower and upper
   block bounds over the planned 48 blocks.
4. Do not impute failed trajectories into the observed-complete estimate; the
   completion range is a missing-outcome bound, not a confidence interval.

The convention is implemented in `tools/candidate_a_structural.py` and in the
sealed continuation runner's `analyze` function. Re-running the reproduction
returns the frozen ranges:

| estimand | full-grid completion range |
|---|---:|
| `D_asym` | `[-3.1987847222, 4.8415798611]` |
| `J` | `[-4.8914930556, 5.6879340278]` |

The original launch record does not contain a dated pre-analysis selection of
this convention. Accordingly, A5 remains a provenance limitation even though
the numerical convention is now explicit and reproducible.
