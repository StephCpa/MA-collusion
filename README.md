# Multi-agent coordination: AAMAS 2027 paper materials

This repository contains the anonymous, paper-facing materials for the AAMAS
2027 history-display observability study.

## Contents

- `paper-materials/aamas2027/latex/`: anonymous LaTeX source and bibliography.
- `paper-materials/aamas2027/figures/`: source figures in PDF/PNG plus manifests
  and captions.
- `paper-materials/aamas2027/analysis/`: frozen analyses, reviewer-response
  qualifications and offline baseline reports.
- `paper-materials/aamas2027/data/`: the A confirmation analysis, status and
  trajectory ledger used for the reported missingness-sensitive result.
- `paper-materials/aamas2027/protocols/`: confirmation and mechanism protocols.
- `paper-materials/aamas2027/aamas2027-supplement-v0.1.zip`: anonymous
  supplementary package for review.

## Evidence boundary

The materials support a bounded claim about how history-display interventions
change observable joint-action structure and seller allocation inside welfare-
equivalence classes in the tested LLM pricing environment. They do not, by
themselves, establish collusion, intent, general punishment, cross-model
external validity, or a general monitoring false-negative rate.

Candidate A was executed in two sealed segments after a transport failure and
local ledger-write failure. The combined record contains 376/384 complete
trajectories and 8 failed trajectories; the missingness-sensitive result is
reported in `analysis/A-confirmation-result-20261001.md`.

## Exclusions

Raw provider request/response logs, API credentials, private filesystem paths,
and local execution snapshots are intentionally excluded. The supplementary
ZIP contains the sanitized scripts and summaries intended for reviewers.

## Reproduction note

The LaTeX source currently reflects the anonymous staging build. Before formal
submission, migrate it to the official AAMAS template without modifying the
venue style files, then rerun the page-count and anonymity checks.
