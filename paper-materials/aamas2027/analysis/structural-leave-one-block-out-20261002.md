# Structural primary: leave-one-block-out sensitivity

Using the same 42 complete blocks and the registered block-level estimand, we
recomputed the mean after deleting each block in turn. The full estimate is
`D_tie = 0.8304`; the 42 leave-one-out means range from `0.8262` to `0.8500`,
and every one remains positive. The lowest leave-one-out estimate occurs when
block 1 is retained out, and the highest when block 19 is retained out.

This is a descriptive influence check. It does not replace the registered
block-$t$ interval or the missing-outcome completion range, and it does not
alter the primary analysis.
