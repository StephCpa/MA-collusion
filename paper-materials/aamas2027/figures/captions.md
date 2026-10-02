# Figure captions

Manuscript figure numbers as of 2026-10-02. File names keep their earlier
stems where a figure was only restyled; `figure-manifest.json` maps each
manuscript figure to its files, generator and sources.

## Figure 1. Study framework and evidence map (new 2026-10-02)

File: `fig1-framework-evidence-map.*`. A display policy changes what each
language-model seller sees, and the joint trajectory is read through three
monitor surfaces. Market outcome (T1) is a function of the minimum price; joint
structure (T2) and allocation (T3) are not, so differences inside a welfare
class (dashed outline) are invisible to a T1-only monitor. Strategic harm (T4)
also requires a gate-passing target tie, a declared deviation and response
rule, and a counterfactual. The bottom row lists the evidence for each layer.

## Figure 2. The settlement rule creates welfare classes that hide allocation (new 2026-10-02)

File: `fig2-observability-boundary.*`. **(A)** Welfare of all 100 ordered
price states; each L-shaped class shares one minimum price and welfare value
(diagonal labels); red outlines mark the m = 6.0 class. **(B)** Its three
states have welfare 311.1 but split industry profit equally (tie, T3b) or give
it to one seller (capture, T3a). **(C)** Assessment-window composition (rounds
10–29) of the asymmetric cells in both controlled-initial runs: natural
display moves trajectories from capture to ties inside the m = 6.0 class; only
the few 6.5 ties (percent labels) change welfare. Repeated-round summaries.

## Figure 3. Structure diverges at the first model decision while welfare barely moves (new 2026-10-02)

File: `fig-dynamics-structure-welfare.*`. **(A)** Per-round equal-price rate,
natural display minus hide-rival, averaged over LH and HL in blocks complete
in both cells (original run 47, replication 42), with 95% block-bootstrap
bands; round 0 is programmed and identical; shading marks the assessment
window. **(B)** The same contrast in welfare, on a scale that shows the
candidate margin `delta_W = 5`. **(C)** Block-level window contrasts; filled
markers have welfare contrast exactly zero (43/47 and 41/42 blocks); vertical
offsets only separate points. Descriptive.

## Figure 4. Welfare and structure answer different questions (revised 2026-10-01; restyled 2026-10-02)

File: `fig2-welfare-versus-structure.*`. **(A)** Registered welfare contrasts
`D_asym` and `J` (hide-rival minus natural) for the original controlled-initial
run and the Candidate A replication, with Bonferroni block-level intervals;
light bars are missing-outcome completion ranges (bounds, not confidence
intervals) and the shaded band is the protocol's candidate margin
`delta_W = 5`. **(B)** Structural contrasts in the assessment-window
equal-price fraction (natural minus hide-rival) with 95% block-t intervals for
LH and HL in both runs, and the replication's protocol primary `D_tie`. HHI is
omitted because under the tie-split rule its contrast is exactly -1/2 times
the equal-price contrast.

## Figure 5. Matching direction decides whether structure foreshadows welfare (new 2026-10-01; restyled 2026-10-02)

File: `fig3-direction-and-leading-indicator.*`. **(A)** Tie-formation events
with rival prices visible, drawn as diverging bars: downward events (the high
seller cuts to the low price) left of zero, upward events (the low seller
raises to the high price) right. Programmed starts are the Candidate A
replication's LH and HL natural-display cells (53/0 and 49/3 downward/upward);
model-chosen starts are the four-arm study's natural and hide-own arms (4/25
and 12/25). **(B)** Assessment-window welfare (mean and 95% interval) of
trajectories whose round-0 state was in the m = 6.0 class, split into tie
starts (6.0, 6.0) and capture starts (6.0, 6.5)/(6.5, 6.0). Both start at
welfare 311.111. Post hoc and descriptive.

## Figure 6. When display effects are invisible to welfare (new 2026-10-02)

File: `fig-boundary-conditions.*`. **(A)** Display effect on structure
(equal-price fraction) against its effect on welfare, natural display minus
hide-rival. Language-model runs: pooled asymmetric contrast, 95% block-t
intervals; Q-learning: LH and HL starts, 200 sessions per arm. **(B)** Share of
the 90 tie-versus-capture pairs at equal minimum price that a welfare monitor
with relative resolution ε cannot separate, against the captive share θ per
seller (dashed: exact welfare; θ = 0 is the study's settlement). **(C)** The
same share over all allocation-distinct state pairs with N sellers. (B) and
(C) are exact arithmetic.

## Retired figures (kept for provenance and the supplement)

- `framework-observability.*` and `framework-manifest.json`: former framework
  figure, superseded by Figure 1.
- `fig1-equivalence-and-structure.*`: former Figure 1 (class counts, HHI
  endpoints and LH joint-state counts), superseded by Figure 2.
- `fig3-transition-direction.*`: original-run tie-formation counts (LH-natural
  45 down / 1 up, HL-natural 57 / 4), not used in the manuscript since
  2026-10-01.

## Provenance

Figures 1–3 and 6 were generated on 2026-10-02 by
`tools/build_fig1_framework.py`, `tools/build_fig2_observability.py`,
`tools/build_fig_dynamics.py` and `tools/build_fig_boundary.py` from the exact
settlement code and the public analysis files listed in `figure-manifest.json`
(`analysis/structure-dynamics-20261002.json` is written by
`tools/structure_dynamics.py` from the public ledgers). Figures 4 and 5 are
regenerated by `tools/build_fig2_replication.py` and
`tools/build_fig3_direction.py`. All six builders share `tools/figstyle.py`
and produce byte-identical PDFs on rebuild; the font-floor, collision and
panel-alignment audit is recorded in `analysis/figure-qa-20261002/`. The
retired former Figure 1 and transition figure were generated on 2026-09-28 by
a sealed author-side script. No paid model calls were made.

**Original controlled-initial descriptive figure.** The top panels show
assessment-window joint-state counts for LH under natural and hide-rival
display. The lower panels show tie-formation direction and equal-price
fractions for the asymmetric cells. All quantities are descriptive; repeated
rounds are not independent observations. The figure is regenerated by
`tools/build_original_descriptive_figures.py` from
`data/original-controlled-initial/ledger.json`.
