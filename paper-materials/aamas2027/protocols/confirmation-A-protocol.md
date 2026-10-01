# Candidate A: independent confirmation and practical-equivalence protocol

**Status (updated 2026-10-01):** executed as an amended two-segment run
(376/384 complete, 8 failed; see `analysis/A-confirmation-result-20261001.md`
and `analysis/A-confirmation-structural-20261001.md`).  The protocol text
below is preserved as frozen before launch; it was not edited after the
results were seen.  Its original status line read: "offline candidate only;
not registered and not launched.  No model calls are authorized by this
document."  The record of when $\delta_W=5$ was selected (required below
"before any call") is not included in these materials and should be attached
from the launch manifest; until it is, the paper describes $\delta_W=5$ as the
protocol's candidate margin.

## Purpose

Candidate A is the confirmatory follow-up for the two claims that can be
separated cleanly in the current record: (i) the history-display intervention
changes structural joint-action outcomes in the asymmetric initial states, and
(ii) the corresponding welfare movement is practically small at the tested
operating point.  The two estimands must not be merged.  A positive structural
effect does not imply a positive welfare effect, and a welfare-equivalence
result does not imply state or allocation equivalence.

## Design candidate

Use the existing controlled-initial eight-cell design, with natural versus
hide-rival display crossed with LL, LH, HL and HH programmed initial states.
Use 48 complete matched blocks, 384 planned trajectories and 22,272 planned
model calls, matching the frozen power-budget candidate.  The block, not the
individual trajectory or request, is the independent unit.  Keep the model,
temperature, token cap, schema, horizon, request order, stopping rule,
missingness ledger and provider configuration fixed to the prior run.  Do not
pool the new run with the old run for the primary interval.

## Frozen estimands (candidate defaults)

1. **Structural primary:** the natural-minus-hide-rival contrast in equal-price
   persistence, reported separately for LH and HL and as their pre-specified
   average $D_{\mathrm{tie}}$.  Report the block-level effect, two-sided 95%
   interval, and completion-range sensitivity.
2. **Welfare equivalence:** the registered welfare contrasts $D_{asym}$ and
   $J$, each tested against a practical equivalence margin rather than by a
   non-significance claim.  Candidate default margin: $\delta_W=5$ welfare
   units on the 20-round assessment window.  This value is a proposal for
   approval, not an established scientific constant.
3. **Allocation guardrail:** report seller-share disparity and HHI as
   descriptive structural outcomes.  They are not substituted for welfare and
   are not interpreted as collusion evidence.

Before any call, select one $\delta_W$ and record the rationale.  Sensitivity
values (3 and 10 welfare units) may be shown descriptively, but only the
pre-selected value may determine the confirmatory equivalence decision.

## Analysis and missingness

Compute trajectory means over rounds 10--29, then form block-level contrasts.
Use the same Bonferroni family for $D_{asym}$ and $J$ as in the current
protocol.  Report observed-complete estimates and a completion-range bound
using the full welfare support for unresolved trajectories.  Do not impute
failures into the primary estimate, do not stop and silently replace a failed
block, and do not treat a zero-width bootstrap interval as a population claim.
The run is invalid for the confirmatory decision if the sealed request schema,
model fingerprint, or planned-cell ledger changes after launch.

## Decision rules

- Structural confirmation: the pre-specified 95% interval for
  $D_{\mathrm{tie}}$ excludes zero in the registered direction, subject to
  the completion-range report.
- Welfare equivalence: both $D_{asym}$ and $J$ must have their full 95%
  intervals contained in $[-\delta_W,+\delta_W]$.  If either interval crosses
  the margin, report inconclusive rather than equivalent.
- Any failure-rate, completion-range or prompt-surface anomaly is reported
  before interpreting a null result.

## Budget and approval gate

The 48-block candidate has 22,272 planned calls.  The prior conservative
budget record quotes approximately 134.70--223.79 yuan under the stated
DeepSeek-flash token scenarios, with a 250-yuan upper reservation.  These are
planning figures, not a live price quote.  Before launch, re-check the current
provider price, freeze the model alias and fingerprint, run the offline
runner/ledger self-tests, and record explicit approval for this new paid batch.

This protocol does not authorize Candidate B, a second model family, lower
initial states, or any strategic-maintenance/T4 claim.
