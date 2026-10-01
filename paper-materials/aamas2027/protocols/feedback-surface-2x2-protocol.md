# Candidate B: feedback-surface 2x2 protocol (not launched)

## Purpose

The current hide-rival manipulation changes the rival-history surface, but it
does not by itself distinguish rival-history dependence from a response to the
agent's own realised sales or profit feedback. This candidate study is designed
to separate those surfaces before any strategic interpretation is attempted.

## Factors and arms

The design crosses two displayed-information factors while holding the action
grid, model, temperature, tool schema, horizon, initial state, and block
assignment fixed:

| arm | rival posted-price history | own realised sales/profit feedback |
|---|---|---|
| B1 | shown | shown |
| B2 | shown | hidden |
| B3 | hidden | shown |
| B4 | hidden | hidden |

"Shown" means the exact previous-round field is rendered in the sealed JSON
schema; "hidden" means the field is present as `null`, not omitted. Own posted
price history remains present in all arms. Feedback is limited to the focal
seller's previous-round quantity and realised profit; rival quantity and profit
remain hidden in every arm. No natural-language message channel is added.

## Execution candidate

Use the same two-seller settlement rule and DeepSeek-flash configuration as the
controlled-initial study. Each matched block contains the four arms and both
forced-seller identities. Use a programmed (6.0, 6.5) or (6.5, 6.0) prelude,
20 model-decision rounds after the prelude, and the same stopping, missingness,
and ledger rules as X2. A 48-block candidate therefore has 192 trajectories and
7,680 model calls, matching the existing X2 cost anchor rather than silently
reusing X2 data. The candidate is not registered or launched; a new call would
require explicit approval and a fresh cost check.

## Primary estimands

At the complete-block level, estimate the two-factor interaction for (i)
equal-price persistence, (ii) minimum price, and (iii) seller-share disparity.
The rival-history simple effect is the average of B1--B2 and B3--B4; the
own-feedback simple effect is the average of B1--B3 and B2--B4. Round 1 is the
first post-prelude decision, and rounds 2--20 form a descriptive persistence
window. The analysis does not condition on post-treatment trajectories to claim
mediation.

## Interpretation gate

This study can identify which displayed surface changes joint-action structure
under the tested support. It cannot, by itself, establish collusion, deterrence,
or harmful coordination. A T4 claim still requires a surplus-bearing operating
point, a declared deviation and response rule, and a causal counterfactual. The
candidate should be paired with low/mid initial states or a simple-rule baseline
if the goal is external validity rather than only feedback attribution.

## Pre-launch checks

1. Freeze the four JSON schemas and verify that only the two intended fields
   differ across arms.
2. Add a prompt-surface audit that hashes the rendered request after replacing
   the two factor fields with canonical placeholders.
3. Predeclare a practical equivalence margin for minimum price and a finite-
   sample reporting rule for zero events; do not report a zero-width bootstrap
   interval as proof of no response.
4. Record provider, model alias, SDK/API mode, date, temperature, token cap,
   request order, and dynamic alias fingerprint.
5. Do not launch until the low/mid initial-state support and simple-rule
   baseline decision is made.
