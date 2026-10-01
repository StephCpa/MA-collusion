# Materials manifest

## Manuscript

- `latex/history-display-observability.tex` — anonymous eight-page staging source (revised 2026-10-01).
- `latex/history-display-observability.bib` — bibliography used by the source.
- `latex/history-display-observability-staging.pdf` — compiled staging build (acmart, 8 pages including references).

## Figures

- `figures/fig1-equivalence-and-structure.*` (original run)
- `figures/fig2-welfare-versus-structure.*` (regenerated 2026-10-01 with the replication; `tools/build_fig2_replication.py`)
- `figures/fig3-transition-direction.*` (original run)
- `figures/framework-observability.*`
- accompanying captions and figure manifests.

## Evidence and analysis

- controlled-initial follow-up report and analysis (private source paths replaced by project-relative paths on 2026-10-01; no values changed);
- Candidate A confirmation result record (corrected 2026-10-01) and raw trajectory ledger;
- Candidate A structural primary and descriptive record (`analysis/A-confirmation-structural-20261001.*`, new);
- settlement observability certificate and operating-point gate (`analysis/observability-certificate.*`, new);
- X1/X2 statistical qualification (gap-direction label corrected);
- fixed-history qualification;
- offline initial-state baseline ("absorbing" wording removed);
- reproducibility metadata register.

## Tools (offline; no provider calls)

- `tools/observability_certificate.py` — derives the T1 partition and separating observables, evaluates the T4 operating-point gate, re-settles every ledger round.
- `tools/candidate_a_structural.py` — reproduces `data/A-confirmation-analysis.json` exactly (never writes it) and computes the protocol structural primary `D_tie`.
- `tools/build_fig2_replication.py` — regenerates Figure 2 byte-reproducibly.
- `tools/check_materials.py` — manuscript-to-analysis number check, citation/figure check, anonymity scan, optional PDF page/overfull check.

## Protocols and supplement

- Candidate A independent-confirmation protocol (execution status note added; frozen text preserved);
- B1--B4 feedback-surface 2x2 protocol;
- anonymous AAMAS supplementary ZIP v0.2 (current) and v0.1 (unchanged, for provenance).

## Review response

- `REVIEW-RESPONSE-20261001.md` — point-by-point response and the list of corrections.

Raw provider request/response logs are excluded by design. The trajectory
ledger is included because it is the primary data object needed to inspect the
reported missingness, completion-range and structural-primary analyses.
