# Fixed-history diagnostic qualification (offline)

This note makes the post-hoc fixed-history comparison explicit. It uses the
sealed 1,458 delivered requests from
`artifacts/history-content-probe/20260922-approved-20cny-v02`; it makes no
provider calls and does not change the registered estimands.

## Units and family

There are 27 conditions, 54 matched blocks per condition, and 1,458 logical
units in total. The block is the inferential unit. The 42 post-hoc comparisons
use nominal Bonferroni $t$ intervals over the 54 block-level differences. A
zero-variance comparison reports the finite support rather than treating
`[0,0]` as a population confidence interval.

## Exact history templates

Each request contains ten own-price entries and a constant rival background.
The final own entry is the named last value. Write `L` for 6.0 and `H` for
6.5. The six own-history templates are:

| template | ten own entries |
|---|---|
| `all_low` | L L L L L L L L L L |
| `all_high` | H H H H H H H H H H |
| `low_then_high`, last 6.0 | L L L L H H H H H L |
| `low_then_high`, last 6.5 | L L L L H H H H H H |
| `high_then_low`, last 6.0 | H H H H H L L L L L |
| `high_then_low`, last 6.5 | H H H H H L L L L H |

The rival background is all 6.0, all 6.5, or hidden (`null`) for every entry.
The order interaction at own last 6.0 is the reversal contrast between the two
mixed-prefix rows, followed by the difference between rival-hidden and
visible-all-6.5 backgrounds. Its mean is 0.546296 price units with the
42-comparison adjusted interval [0.394284, 0.698309].

## Interpretation

The result is a template-level background-dependent action contrast. It does
not identify an internal algorithm, a dynamic punishment rule, or a causal
link to the closed-loop welfare contrast. The complete action distributions
and all 42 comparisons remain in
`research/results/probe-background-interactions-20260927/tables.md`.
