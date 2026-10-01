# Multi-agent coordination: AAMAS 2027 paper materials

This repository contains the anonymous, paper-facing materials for the AAMAS
2027 history-display observability study.

## Contents

- `paper-materials/aamas2027/latex/`: anonymous LaTeX source, bibliography and
  a compiled staging PDF (`history-display-observability-staging.pdf`).
- `paper-materials/aamas2027/figures/`: source figures in PDF/PNG plus manifests
  and captions.
- `paper-materials/aamas2027/analysis/`: frozen analyses, reviewer-response
  qualifications, offline baseline reports, the settlement observability
  certificate and the Candidate A structural analysis.
- `paper-materials/aamas2027/data/`: the Candidate A analysis, status and
  trajectory ledger, and the four-arm history-channel ledger and analysis.
- `paper-materials/aamas2027/protocols/`: confirmation and mechanism protocols.
- `paper-materials/aamas2027/tools/`: offline scripts that regenerate the
  certificate, the Candidate A analysis, the four-arm leading-indicator and
  blindness analysis, the settlement generalization, the Q-learning baseline
  and Figures 2–3, plus a consistency gate.
- `paper-materials/aamas2027/aamas2027-supplement-v0.3.zip`: anonymous
  supplementary package for review (v0.1 is kept unchanged for provenance).
- `paper-materials/aamas2027/REVIEW-RESPONSE-20261001.md`: response to the
  latest review and the list of corrections in this revision.

## Evidence boundary

The materials support a bounded claim about how history-display interventions
change observable joint-action structure and seller allocation inside welfare-
equivalence classes in the tested LLM pricing environment, and an independent
within-deployment replication of that structural contrast. They do not, by
themselves, establish collusion, intent, general punishment, cross-model
external validity, or a general monitoring false-negative rate.

Candidate A was executed in two sealed segments after a transport failure and
local ledger-write failure; the continuation was authorized after an
interruption and an inspection of interim results. The combined record
contains 376/384 complete trajectories and 8 failed trajectories. Its
structural primary is confirmed (`D_tie` = 0.830, 95% block-t [0.743, 0.917]);
its welfare-equivalence decision is inconclusive under the registered
missingness sensitivity. See `analysis/A-confirmation-result-20261001.md` and
`analysis/A-confirmation-structural-20261001.md`.

## Reproduction

All checks are offline and make no provider calls. From the repository root
(Python 3.10+; `matplotlib` only for the figure):

```text
python paper-materials/aamas2027/tools/observability_certificate.py --check --write
python paper-materials/aamas2027/tools/candidate_a_structural.py --check --write
python paper-materials/aamas2027/tools/four_arm_leading_indicator.py --check --write
python paper-materials/aamas2027/tools/settlement_generalization.py --check --write
python paper-materials/aamas2027/tools/qlearning_baseline.py --write      # about 15 minutes
python paper-materials/aamas2027/tools/build_fig2_replication.py
python paper-materials/aamas2027/tools/build_fig3_direction.py
python paper-materials/aamas2027/tools/check_materials.py
```

`check_materials.py` fails if a number quoted in the manuscript drifts from the
analysis file it comes from, a citation or figure is missing, or a private
path, e-mail address or key-like string appears in the materials or the
supplement. With `--pdf <build.pdf> --log <build.log>` it also checks the
8-page limit and overfull boxes. To build the staging PDF, run `pdflatex`,
`bibtex`, `pdflatex`, `pdflatex` in `paper-materials/aamas2027/latex/`.

## Exclusions

Raw provider request/response logs, API credentials, private filesystem paths,
and local execution snapshots are intentionally excluded. The supplementary
ZIP contains the sanitized scripts and summaries intended for reviewers.

## Before submission

The LaTeX source reflects the anonymous staging build. Before formal
submission, migrate it to the official AAMAS template without modifying the
venue style files, then rerun the page-count and anonymity checks. This
repository's commit metadata is not anonymous; do not link it from the
submission (use an anonymized mirror for the supplement if a link is needed).
