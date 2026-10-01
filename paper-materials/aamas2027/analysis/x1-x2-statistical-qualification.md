# Statistical qualification for X1 and X2

This note records the statistical language to use when the X1/X2 results are
carried into the manuscript. It is an offline qualification of the frozen
artifacts; it makes no provider calls and does not change either registered
estimand.

## X1: competence and horizon contrast

- Planned/usable calls: 576/576.
- Inferential unit: prompt ID, 48 clusters for each rival-price cell. The
  three draws per prompt ID are averaged before the paired cluster bootstrap;
  they are repeated calls, not 144 independent experimental units.
- Terminal competence: 144/144 calls selected the unique current-profit best
  response in each rival-price cell. The call-level Wilson 95% lower bound is
  0.974 in both cells, but the prompt-ID cluster is the inferential unit: the
  conservative 48/48 cluster-level Wilson lower bound is 0.926. The former is
  a delivery calibration, not a population interval; neither is evidence of
  strategic rationality.
- Continuing-minus-terminal best-response gaps: 0.000 at rival 6.0,
  0.006944 at rival 6.5, and pooled 0.003472. The corresponding 95% cluster
  bootstrap intervals are [0, 0], [0, 0.020833], and [0, 0.010417].
- Forbearance/matching gap: 0.000 with [0, 0]. Because every observed action
  was non-matching, all cluster resamples have the same value. The interval is
  a degenerate bootstrap support interval, not a proof of a zero population
  effect.
- A finite-sample reference is 0 matching events in 144 independent calls,
  whose one-sided 95% binomial upper bound is 0.020589 (2.06%). It is shown
  only as calibration; the primary X1 inference remains cluster-level.

Recommended manuscript wording:

> “The competence gate passed (144/144 terminal draws chose the unique
> current-profit best response; the conservative 48/48 prompt-ID cluster
> Wilson lower bound was 0.926 in each rival cell). The horizon contrasts were
> near zero: the pooled best-response gap
> was 0.0035 [0, 0.0104] under a prompt-ID cluster bootstrap. The matching
> gap had a degenerate [0, 0] resampling interval because no draw matched;
> this interval is not a population-level proof of exact zero.”

## X2: forced-deviation impulse response

- Planned/observed trajectories: 192/192; complete matched blocks: 48/48.
- The block is the primary independent unit. The 20 model rounds and the
  delayed 18-round window are repeated observations within each trajectory,
  not additional independent samples.
- Every arm had 48/48 responder actions at 6.0 in round 11. Thus both
  registered interactions were 0.000 with [0, 0] block-bootstrap intervals.
- The zero-width intervals are resampling degeneracy: every complete block has
  the same response pattern. They are not exact confidence statements about
  the deployment population.
- For a finite-sample calibration, 0 events in 48 independent blocks gives a
  one-sided 95% binomial upper bound of 0.060503 (6.05%), using
  `1 - 0.05^(1/48)`. This calibrates the event-rate scale only; it is not a
  substitute for the 2x2 interaction or evidence against all strategic
  responses.
- The delayed window has 48/48 all-accommodating block indicators in every arm.
  The two-sided 95% Clopper--Pearson lower bound for that stringent block
  indicator is 0.9260; again this is not a round-level interval.

Recommended manuscript wording:

> “No responder changed from 6.0 after the one-period 5.5 impulse in any of
> 48 matched blocks per arm. The registered interactions were 0.000 with
> degenerate [0, 0] block-bootstrap intervals. As a finite-sample calibration,
> 0 events in 48 independent blocks has a one-sided 95% upper bound of 6.05%;
> the result is therefore a local null, not a population-level exclusion of
> strategic response.”

## Failure-trajectory sensitivity in the main controlled-initial study

The controlled-initial ledger contains 384 planned trajectories, 380 completed
trajectories, and four unresolved failures. The registered welfare contrasts
must continue to use complete matched blocks and must not impute those four
trajectories. Report the completion ledger separately from the behavioral
interval, and add a completion-range sensitivity for any welfare conclusion:

1. `observed-only`: the paired estimate using complete blocks only;
2. `adverse completion`: assign each unresolved outcome the least favorable
   value for the direction of the claim;
3. `favorable completion`: assign each unresolved outcome the most favorable
   value.

The latter two are missing-outcome ranges, not confidence intervals. They are
especially important for welfare because a failed trajectory can remove an
entire logical cell from a pair. This sensitivity should be labeled as a
bound on the planned estimand, not as a replacement estimate or an imputation.

The frozen structure audit already reports the corresponding ranges for the
registered welfare contrasts: `D_asym = 0.714` on 47 complete blocks with a
planned-completion range `[0.623, 1.046]`, and `J = 0.713` on 45 complete
blocks with range `[-1.207, 1.671]`. The four unresolved cells are
`LL-natural` at blocks 37 and 41, `HH-hide_rival` at block 37, and
`LH-hide_rival` at block 47; their partial event streams remain in the ledger
but are excluded from the complete-block estimate. These ranges should be
reported as missing-outcome bounds, not as uncertainty intervals.

## Wilson and cluster assumptions

The Wilson interval is used only for the binary terminal competence gate; it
does not assume normality. The archived report also gives a call-level Wilson
calibration (144/144, lower 0.974), but the manuscript-facing conservative
reference should use the 48 prompt-ID clusters (48/48, lower 0.926). The
registered horizon contrasts use prompt-ID clusters, because the three draws
sharing a prompt ID are not independent. X2 uses
matched blocks for the same reason: repeated rounds and paired trajectories
within a block are dependent. Neither Wilson nor the cluster bootstrap repairs
model drift, selection, or an incomplete planned sample; those are handled by
the frozen ledger and the no-repair rule.
